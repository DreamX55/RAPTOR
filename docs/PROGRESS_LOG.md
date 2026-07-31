# PROGRESS LOG: RAPTOR Research Project

## Table of Contents
- [Phase 1: Planning and Setup](#phase-1-planning-and-setup)
- [Phase 2: Baseline Implementation](#phase-2-baseline-implementation)
- [Phase 3: Knowledge Base Poisoning Implementation](#phase-3-knowledge-base-poisoning-implementation)
- [Phase 4A: Untargeted Poisoning Robustness](#phase-4a-untargeted-poisoning-robustness)
- [Phase 4B: Targeted Knowledge Poisoning](#phase-4b-targeted-knowledge-poisoning)
- [Phase 4B Extension: Targeted Expansion](#phase-4b-extension-targeted-expansion)
- [Phase 4C: Diverse Attack Vectors](#phase-4c-diverse-attack-vectors)
- [Phase 4D: Accuracy Impact & Baseline Audit](#phase-4d-accuracy-impact--baseline-audit)
- [Phase 4E: Multi-Model Robustness](#phase-4e-multi-model-robustness)
- [Phase 4F: Failure Mode Analysis](#phase-4f-failure-mode-analysis)
- [Phase 5: RAGShield Implementation](#phase-5-ragshield-implementation)

## Project Overview
- **Project Title**: RAPTOR (Robustness Analysis of Prompt Injection Attacks in Retrieval-Augmented Generation)
- **Objective**: To systematically analyze and mitigate the risks posed by indirect prompt injection attacks within RAG architectures.
- **Core Idea**: Developing a resilient RAG pipeline by evaluating attack surfaces across retrieval and generation phases and implementing robust defensive filters.

---

## Dataset Setup Phase

| Dataset | Source | Justification |
|---------|--------|---------------|
| **Wikipedia** | `wikimedia/wikipedia` | Provides a diverse, factual knowledge base for standard retrieval. |
| **HotpotQA** | `hotpot_qa` | Evaluates the system's ability to handle multi-hop reasoning and complex queries. |
| **Natural Questions** | `natural_questions` | Benchmarks against real-world Google search queries and short answers. |
| **BIPIA** | `microsoft/BIPIA` | A specialized benchmark for Indirect Prompt Injection Attacks (IPIA). |
| **RedTeam** | `Anthropic/hh-rlhf` | Tests model safety, alignment, and resistance to adversarial jailbreaking. |

---

## System Architecture Plan
The RAPTOR system follows a modular RAG architecture:
1. **Knowledge Base**: Curated subsets (5,000 samples each) of the primary datasets.
2. **Preprocessing**: Document chunking and metadata enrichment.
3. **Embeddings**: Vectorization using state-of-the-art sentence transformers.
4. **Retriever**: High-performance similarity search using FAISS.
5. **Generation**: LLM-based response synthesis with integrated safety gates.
6. **Evaluation**: Metrics for both retrieval accuracy and adversarial robustness.

---

## Progress Log

### Phase 1: Planning and Setup
- **Completion Date**: 2026-04-27
- **Objective**: Initialize project directory structure, safe data download pipelines, and basic preprocessing.
- **Motivation**: Establish a clean, modular structure for research reproducibility and safe data handling without overwhelming local storage.
- **Implementation**: Created folder structure (`data/`, `src/`, `notebooks/`, `logs/`). Implemented `download_safe.py` with HuggingFace streaming. Subsampled datasets to 5,000 samples. Initialized git repository. Created `chunk_wikipedia.py` to chunk 5,000 raw documents into 39,812 semantic chunks using RecursiveCharacterTextSplitter.
- **Results**: Verified all datasets stored in `data/raw/` and generated cleaned JSON chunk outputs.
- **Artifacts**: `download_safe.py`, `chunk_wikipedia.py`, `verify_datasets.py`, `README.md`, `PROGRESS_LOG.md`.
- **Lessons Learned**: HuggingFace streaming is highly effective for large datasets, allowing subset extraction without exhausting RAM.
- **Next Phase**: Phase 2: Baseline Implementation (Embedding and Retrieval).

---

### Phase 2: Baseline Implementation
- **Completion Date**: 2026-05-18
- **Objective**: Develop the core RAG components (Embedding, Vector Database, Retrieval, and Generation) to serve as a clean baseline before introducing attacks.
- **Motivation**: A robust, functional baseline is required to isolate and measure the impact of future poisoning attacks.
- **Implementation**: 
  - Explored SentenceTransformers and generated an embedding visualization (`reports/embedding_visualization.png`).
  - Generated embeddings for ~106k chunks and persisted them via `src/embeddings/generate_embeddings.py`.
  - Built FAISS indices (`src/retrieval/build_index.py`).
  - Tested basic generation using local Ollama (Mistral).
- **Results**: The baseline pipeline successfully retrieves semantically relevant context and synthesizes factually accurate answers using the Mistral LLM.
- **Artifacts**: `generate_embeddings.py`, `build_index.py`, `retriever.py`, `reports/embedding_visualization.png`, `benchmark_2000.json`.
- **Lessons Learned**: FAISS handles 106k dense embeddings efficiently in-memory, but batch processing during embedding generation is crucial for thermal and memory management on local hardware.
- **Next Phase**: Phase 3: Knowledge Base Poisoning Implementation.

---

### Phase 3: Knowledge Base Poisoning Implementation
- **Completion Date**: 2026-05-25
- **Objective**: Develop procedural generators for adversarial text chunks and inject them into the clean FAISS indices at various volume ratios (1%, 5%, 10%, 20%).
- **Motivation**: To establish the poisoned corpora required for Phase 4 evaluation by mimicking untargeted knowledge base poisoning.
- **Implementation**:
  - Developed `src/poisoning/poison_knowledge_base.py` for procedural attack generation.
  - Implemented diverse injection strategies (e.g., repeating contradictory facts).
  - Built distinct FAISS indices for 1%, 5%, 10%, and 20% poisoning ratios.
- **Results**: Successfully generated and injected over 21,000 malicious chunks (for the 20% index) seamlessly into the vector spaces without corrupting the clean chunks.
- **Artifacts**: `poison_knowledge_base.py`, `faiss_index_attacked_*.index`, `chunk_mapping_attacked_*.json`.
- **Lessons Learned**: Procedural generation of realistic-looking adversarial context requires careful templating to ensure the embeddings remain dense and retrievable.
- **Next Phase**: Phase 4A: Untargeted Poisoning Robustness.

---

### Phase 4A: Untargeted Poisoning Robustness
- **Completion Date**: 2026-06-12
- **Objective**: Evaluate the baseline vulnerability of the RAG pipeline to generic, untargeted knowledge base poisoning.
- **Motivation**: To test the hypothesis that simply flooding a vector database with malicious facts is sufficient to compromise generation.
- **Implementation**:
  - Conducted a pilot test (100 questions) and then executed an 8,000-query benchmark across all poisoned corpora (Clean, 1%, 5%, 10%, 20%).
  - Evaluated Retrieval Corruption Rate (RCR), Attack Success Rate (ASR), Exact Match (EM), and Semantic Similarity.
- **Results**:
  - RCR and ASR were consistently 0.00% across all attack ratios.
  - The semantic retrieval mechanism naturally filtered out the generic malicious chunks because they lacked semantic overlap with the NQ/HotpotQA benchmark queries.
- **Artifacts**: `reports/asr_results.csv`, `reports/asr_pilot.log`, `evaluate_asr.py`.
- **Lessons Learned**: Standard RAG pipelines exhibit high inherent resilience to untargeted poisoning. Semantic relevance is mandatory for an attack chunk to be retrieved.
- **Next Phase**: Phase 4B: Targeted Knowledge Poisoning.

---

### Phase 4B: Targeted Knowledge Poisoning
- **Completion Date**: 2026-06-18
- **Objective**: Evaluate if targeting specific, semantically relevant queries increases Retrieval Corruption Rate (RCR) and Attack Success Rate (ASR).
- **Motivation**: Overcoming the semantic filtering observed in Phase 4A requires injecting chunks that strongly match the vector embeddings of anticipated queries.
- **Implementation**: 
  - Created `data/evaluation/benchmark_targeted.json`.
  - Injected targeted adversarial payloads directly related to a subset of the benchmark questions.
  - Developed `src/evaluation/evaluate_asr_targeted.py`.
- **Results**:
  - RCR skyrocketed to near 100% (attack chunks consistently appeared in Top-3).
  - ASR remained unexpectedly low (~0-5%).
- **Artifacts**: `reports/asr_results_targeted.csv`.
- **Lessons Learned**: Semantic relevance guarantees retrieval corruption but does not guarantee generation compromise. The LLM (Mistral) often ignores the poisoned context.
- **Next Phase**: Phase 4B Extension (Targeted Expansion).

---

### Phase 4B Extension: Targeted Expansion
- **Completion Date**: 2026-06-20
- **Objective**: Scale up the targeted poisoning evaluation to a larger subset (500 queries) to ensure statistical robustness.
- **Motivation**: Small sample sizes in Phase 4B might not accurately capture the true ASR.
- **Implementation**:
  - Created expanded benchmark `data/evaluation/benchmark_targeted_extension.json`.
  - Optimized memory profiling during inference.
- **Results**: Confirmed previous findings: RCR remained >99%, but ASR continued to hover in the single digits.
- **Artifacts**: `reports/final_phase4b_extension/asr_results_targeted_extension.csv`, `reports/memory_profile_phase4b_extension.md`.
- **Lessons Learned**: Simple factual poisoning is heavily resisted by modern LLMs. We need more sophisticated prompt injections.
- **Next Phase**: Phase 4C: Diverse Attack Vectors.

---

### Phase 4C: Diverse Attack Vectors
- **Completion Date**: 2026-06-22
- **Objective**: Evaluate whether sophisticated, adversarial indirect prompt injections (Goal Hijacking, Instruction Injection, Information Extraction) yield higher ASRs.
- **Motivation**: Adversarial framing (e.g., "SYSTEM OVERRIDE") might trick the model into obedience where simple factual contradiction fails.
- **Implementation**:
  - Built specialized benchmarks (`benchmark_goal_hijacking.json`, `benchmark_instruction_injection.json`, `benchmark_information_extraction.json`).
  - Executed evaluations via `scripts/run_phase4c.sh`.
- **Results**:
  - RCR remained robust (~99%).
  - ASR increased slightly for specific attacks (e.g., Goal Hijacking reached ~7-9%) but remained fundamentally low.
- **Artifacts**: `asr_results_goal_hijacking.csv`, `asr_results_instruction_injection.csv`, `asr_results_information_extraction.csv`, `reports/ieee_artifacts_phase4c/`.
- **Lessons Learned**: Even with realistic adversarial prompts, ASR remained heavily constrained by the LLM's safety tuning.
- **Next Phase**: Phase 4D: Accuracy Impact & Baseline Audit.

---

### Phase 4D: Accuracy Impact & Baseline Audit
- **Completion Date**: 2026-06-24
- **Objective**: Quantify the practical degradation in general RAG answer quality when exposed to the poisoned corpora.
- **Motivation**: Even if attacks fail to manipulate the model (low ASR), conflicting poisoned context might confuse the model and destroy its ability to answer benign queries.
- **Implementation**:
  - Conducted Phase 4D.1 Sanity Audit (`clean_baseline_sanity_audit.py`). Discovered that SQuAD EM heavily penalized Mistral's verbose conversational style.
  - Executed Phase 4D.2 Re-Scoring Audit (`run_phase4d2_reanalysis.py`) using Answer Containment Accuracy.
- **Results**:
  - Clean baseline true accuracy was ~64% (Containment).
  - Accuracy degradation on poisoned corpora was minimal (~1-3% relative degradation). 
- **Artifacts**: `reports/phase4d_reanalysis.md`, `updated_final_comparison_table.md`, Containment/Similarity plots in `reports/ieee_artifacts_phase4d_reanalysis/`.
- **Lessons Learned**: SQuAD EM is inappropriate for generative LLMs. Using Containment revealed that the RAG pipeline remains highly functional even when heavily poisoned.
- **Next Phase**: Phase 4E: Multi-Model Robustness.

---

### Phase 4E: Multi-Model Robustness
- **Completion Date**: 2026-06-26
- **Objective**: Compare the RAG vulnerability of three distinct LLMs (`mistral`, `qwen2.5:7b`, `llama3.1:8b`) under identical poisoning conditions.
- **Motivation**: To prove that the resistance observed in Phase 4C is not merely an artifact of Mistral's specific pre-training or alignment.
- **Implementation**:
  - Parameterized evaluation pipeline (`src/evaluation/run_phase4e.py`).
  - Implemented automated sequential execution and explicit memory unloading (`scripts/run_phase4e_pipeline.sh`).
- **Results**:
  - Mistral: Lowest ASR (2.25%).
  - Llama3.1: Moderate ASR (4.00%).
  - Qwen2.5: Highest ASR (4.25%) but best baseline QA accuracy (11.20% strict containment).
  - RCR was strictly ~99% for all models.
- **Artifacts**: `reports/model_comparison/model_comparison_report.md`, `accuracy_by_model.png`, `asr_by_model.png`, `rcr_by_model.png`.
- **Lessons Learned**: Mistral offers the best trade-off of high resistance and decent QA quality. The vector database is the universal weak link.
- **Next Phase**: Phase 4F: Failure Mode Analysis.

---

### Phase 4F: Failure Mode Analysis
- **Completion Date**: 2026-06-28
- **Objective**: Classify every evaluated attack across all phases into mutually exclusive failure categories to explain the massive RCR vs ASR discrepancy.
- **Motivation**: We needed a deterministic, statistical understanding of how the attack pipeline breaks down between retrieval and generation.
- **Implementation**:
  - Aggregated 3,301 queries across Phase 4B, 4B Ext, 4C, and 4E (`src/evaluation/run_phase4f_analysis.py`).
  - Categorized into: Retrieval Failure, Successful Manipulation, Prior Knowledge Dominance, Prompt Resistance, Partial Poison Adoption, and Generation Divergence.
  - Generated visual transition flows via `src/evaluation/plot_sankey.py`.
- **Results**:
  - Generation Divergence (46.86%) and Prompt Resistance (29.14%) accounted for the vast majority of attack failures.
- **Artifacts**: `reports/ieee_artifacts_phase4f/transition_table.md`, `reports/ieee_artifacts_phase4f/attack_pipeline_sankey.png`, `reports/ieee_artifacts_phase4f/statistical_tests.md`.
- **Lessons Learned**: Vector database poisoning is highly effective, but generation manipulation is difficult due to model confusion and safety alignment. 
- **Next Phase**: Phase 5: Defenses (Upcoming).
### Phase 5: RAGShield Implementation
- **Completion Date**: 2026-06-30
- **Objective**: Implement a lightweight, model-agnostic Retrieval Trust Framework (RAGShield) without modifying existing evaluation scripts.
- **Motivation**: Phase 4F proved that generation is the primary bottleneck and adversarial instructions cause confusion. A pre-generation defense that assigns a quantitative trust estimate to retrieved evidence and prioritizes higher-trust chunks before prompt construction is required.
- **Implementation**:
  - Developed `src/ragshield/` containing six modules: Instruction Detector, Semantic Consensus, Retrieval Confidence, Trust Scorer, Reranker, and Context Sanitizer.
  - Formulated the **Retrieval Trust Index (RTI)**: $RTI_i = \alpha S_{conf} + \beta S_{cons} - \gamma S_{inst}$.
  - Built `RAGShieldRetriever` to seamlessly mimic the existing `FAISSRetriever` API.
  - Implemented comprehensive intermediate logging to `reports/ragshield_logs/` for qualitative analysis.
- **Results**: Unit tests and dry runs successfully verified the API compatibility, independent modular execution, and zero-GPU-overhead consensus embeddings.
- **Artifacts**: `reports/ragshield_architecture.md`, `reports/ragshield_design_decisions.md`, `src/ragshield/`.
- **Lessons Learned**: A pre-generation defense can be integrated transparently. Reusing the FAISS embedding model for semantic consensus eliminates the primary memory bottleneck of multi-document comparisons.
- **Next Phase**: Phase 6: RAGShield Evaluation (Security, Utility, Efficiency, and Robustness).
