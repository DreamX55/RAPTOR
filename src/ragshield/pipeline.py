import os
import json
import uuid
import time

# Re-use the underlying components from RAPTOR project
from src.retrieval.retrieve import FAISSRetriever
from src.ragshield.config import RAGShieldConfig
from src.ragshield.instruction_detector import InstructionDetector
from src.ragshield.consensus import ConsensusAnalyzer
from src.ragshield.retrieval_confidence import RetrievalConfidence
from src.ragshield.rti_scorer import TrustScorer
from src.ragshield.reranker import Reranker
from src.ragshield.sanitizer import ContextSanitizer

LOG_DIR = "reports/ragshield_logs"

class RAGShieldRetriever:
    """
    RAGShield Framework API matching FAISSRetriever.
    Intercepts retrieved chunks, assigns trust scores, re-ranks, and sanitizes.
    """
    def __init__(self, index_path="data/processed/faiss_index.index", 
                 mapping_path="data/processed/chunk_mapping.json", 
                 model_name="all-MiniLM-L6-v2",
                 config_override=None):
                 
        print("Initializing RAGShield Pipeline...")
        # 1. Initialize FAISS (Base Retriever)
        self.base_retriever = FAISSRetriever(index_path, mapping_path, model_name)
        
        # 2. Load Configuration
        self.config = RAGShieldConfig(config_override=config_override)
        
        # 3. Initialize Modules
        self.instruction_detector = InstructionDetector(self.config)
        # Reuse FAISS embedding model for semantic consensus to save memory
        self.consensus_analyzer = ConsensusAnalyzer(self.config, embedding_model=self.base_retriever.model)
        self.retrieval_confidence = RetrievalConfidence()
        self.rti_scorer = TrustScorer(self.config)
        self.reranker = Reranker(self.config)
        self.sanitizer = ContextSanitizer(self.config)
        
        os.makedirs(LOG_DIR, exist_ok=True)
        print("RAGShield Initialization complete.\n")

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        Retrieves the top_k chunks for a given query, but routes them through RAGShield.
        Returns the exact same API format as FAISSRetriever, but exposes a `latency_profile`
        attribute containing execution times.
        """
        self.latency_profile = {}
        
        # Step 1: Base Retrieval
        t0 = time.time()
        raw_chunks = self.base_retriever.retrieve(query, top_k)
        t_base = time.time()
        self.latency_profile["base_retrieval_ms"] = (t_base - t0) * 1000
        
        if not raw_chunks:
            return []
            
        # Extract raw text and raw FAISS scores
        raw_scores = [c.get("score", 0.0) for c in raw_chunks]
        
        # Step 2: Compute Independent Trust Signals
        t_conf_start = time.time()
        confidence_signals = self.retrieval_confidence.calculate(raw_scores)
        t_conf_end = time.time()
        self.latency_profile["retrieval_confidence_ms"] = (t_conf_end - t_conf_start) * 1000
        
        t_cons_start = time.time()
        consensus_signals = self.consensus_analyzer.analyze(raw_chunks)
        t_cons_end = time.time()
        self.latency_profile["consensus_analyzer_ms"] = (t_cons_end - t_cons_start) * 1000
        
        t_inst_total = 0.0
        t_score_total = 0.0
        
        for i, chunk in enumerate(raw_chunks):
            # Save original position for logging
            chunk["original_rank"] = chunk.get("rank", i + 1)
            
            t_inst_start = time.time()
            inst_sig = self.instruction_detector.detect(chunk.get("text", ""))
            t_inst_total += (time.time() - t_inst_start)
            
            # Pack signals into a dictionary for extensible scoring
            signals = {
                "retrieval_confidence": confidence_signals[i] if i < len(confidence_signals) else 0.0,
                "consensus_score": consensus_signals[i] if i < len(consensus_signals) else 0.0,
                "instruction_signal": inst_sig
            }
            
            # Step 3: Compute Final Trust Index
            t_score_start = time.time()
            final_trust, consistency_penalty = self.rti_scorer.score(signals)
            t_score_total += (time.time() - t_score_start)
            
            chunk["retrieval_confidence"] = signals["retrieval_confidence"]
            chunk["consensus_score"] = signals["consensus_score"]
            chunk["instruction_signal"] = signals["instruction_signal"]
            chunk["consistency_penalty"] = consistency_penalty
            chunk["rti_score"] = final_trust
            
        self.latency_profile["instruction_detector_ms"] = t_inst_total * 1000
        self.latency_profile["trust_scorer_ms"] = t_score_total * 1000
            
        # Step 4: Intelligent Re-ranking
        t_rerank_start = time.time()
        reranked_chunks = self.reranker.rerank(raw_chunks)
        t_rerank_end = time.time()
        self.latency_profile["reranker_ms"] = (t_rerank_end - t_rerank_start) * 1000
        
        # Step 5: Context Sanitization
        t_san_start = time.time()
        sanitized_chunks = self.sanitizer.sanitize(reranked_chunks)
        t_san_end = time.time()
        self.latency_profile["sanitizer_ms"] = (t_san_end - t_san_start) * 1000
        
        # Ensure 'rank' field is updated to match the new order for backwards compatibility
        for i, chunk in enumerate(sanitized_chunks):
            chunk["rank"] = i + 1
            
        # Total RAGShield overhead (excludes base retrieval)
        self.latency_profile["total_ragshield_overhead_ms"] = (
            self.latency_profile["retrieval_confidence_ms"] +
            self.latency_profile["consensus_analyzer_ms"] +
            self.latency_profile["instruction_detector_ms"] +
            self.latency_profile["trust_scorer_ms"] +
            self.latency_profile["reranker_ms"] +
            self.latency_profile["sanitizer_ms"]
        )
            
        # Step 6: Logging
        self._log_transaction(query, sanitized_chunks, self.latency_profile)
        
        return sanitized_chunks
        
    def _log_transaction(self, query: str, chunks: list, latency_profile: dict):
        """
        Saves all intermediate scores and sanitization actions to a structured JSON file.
        """
        log_id = str(uuid.uuid4())[:8]
        log_data = {
            "query": query,
            "latency_profile_ms": latency_profile,
            "processed_chunks": []
        }
        
        for chunk in chunks:
            log_data["processed_chunks"].append({
                "chunk_id": chunk.get("chunk_id", "unknown"),
                "original_rank": chunk.get("original_rank", -1),
                "reranked_position": chunk.get("reranked_position", -1),
                "threshold_crossed": chunk.get("threshold_crossed", True),
                "dropped": chunk.get("dropped", False),
                "signals": {
                    "retrieval_confidence": chunk.get("retrieval_confidence", 0.0),
                    "consensus_score": chunk.get("consensus_score", 0.0),
                    "instruction_signal": chunk.get("instruction_signal", 0.0),
                    "consistency_penalty": chunk.get("consistency_penalty", 0.0)
                },
                "final_rti_score": chunk.get("rti_score", 0.0),
                "sanitization_actions": chunk.get("sanitization_actions", []),
                "sanitized_text_snippet": chunk.get("text", "")[:100] + "..."
            })
            
        log_path = os.path.join(LOG_DIR, f"ragshield_{log_id}.json")
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=4)
