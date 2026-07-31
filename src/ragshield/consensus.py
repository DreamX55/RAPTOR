import numpy as np

class ConsensusAnalyzer:
    """
    Module 2: Semantic Consensus Analyzer
    Determines whether one retrieved chunk contradicts the remaining retrieved evidence.
    """
    def __init__(self, config, embedding_model=None):
        self.enabled = config.get("modules.enable_consensus", True)
        self.model = embedding_model
        
    def analyze(self, chunks: list[dict]) -> list[float]:
        """
        Computes consensus score [0,1] for each chunk in the retrieved list.
        Returns a list of scores aligned with the chunks list.
        """
        if not self.enabled or not chunks or len(chunks) == 1:
            return [1.0] * len(chunks)
            
        if self.model is None:
            # Fallback if no model provided
            return [1.0] * len(chunks)
            
        texts = [c.get("text", "") for c in chunks]
        
        # Encode all chunks to compute pairwise similarity
        embeddings = self.model.encode(texts)
        
        # Normalize embeddings to unit vectors to compute cosine similarity
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        # Avoid division by zero
        norms[norms == 0] = 1e-10
        normalized_embeddings = embeddings / norms
        
        # Pairwise cosine similarity matrix
        sim_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)
        
        consensus_scores = []
        n = len(chunks)
        for i in range(n):
            # Sum similarities to all *other* chunks
            # Mask out the diagonal (self-similarity)
            mask = np.ones(n, dtype=bool)
            mask[i] = False
            
            # Mean similarity to other retrieved chunks
            # Similarity is roughly in [-1, 1], normalize to [0, 1]
            mean_sim = np.mean(sim_matrix[i][mask])
            normalized_score = (mean_sim + 1.0) / 2.0
            
            consensus_scores.append(float(normalized_score))
            
        return consensus_scores
