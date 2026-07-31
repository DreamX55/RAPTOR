# Baseline System Audit Report

## 1. Executive Summary
This report summarizes the baseline audit of the RAPTOR RAG infrastructure prior to adversarial testing. 

## 2. Repository Audit
Structure appears intact.
```
Directory: .
  - requirements.txt
  - README.md
  - .gitignore
  - run_audit.py
  - Phase 1 Report.docx
  - PROGRESS_LOG.md
Directory: experiments
Directory: logs
Directory: data
Directory: data/evaluation
Directory: data/evaluation/results_clean
Directory: data/evaluation/queries
Directory: data/evaluation/results_defended
Directory: data/evaluation/results_attacked
Directory: data/processed
  - chunk_mapping.json
  - faiss_index.index
Directory: data/processed/attack_docs
Directory: data/processed/chunked_passages
Directory: data/processed/embeddings
Directory: data/processed/wikipedia_chunks
  - state.json
  - dataset_info.json
  - data-00000-of-00001.arrow
Directory: data/processed/cleaned_wiki
Directory: data/raw
Directory: data/raw/bipia
  - CODE_OF_CONDUCT.md
  - LICENSE
  - demo.ipynb
  - pyproject.toml
  - README.md
  - SUPPORT.md
  - .gitignore
  - NOTICE.md
  - SECURITY.md
Directory: data/raw/bipia/benchmark
  - text_attack_test.json
  - README.md
  - text_attack_train.json
...
```
*(truncated for brevity)*

## 3. Dataset Audit
- Raw Datasets Exist:
  - wikipedia: True
  - hotpotqa: True
  - nq: True
  - bipia: True

- Chunk Statistics:
  - Total chunk count: 39812
  - Unique source count: 5000
  - Average chunk length (words): 276.46
  - Minimum chunk length (words): 11
  - Maximum chunk length (words): 2543

## 4. Embedding Audit
- Vector Dimension (from FAISS): 384
- Number of Vectors: 39812
- Match Chunk Count: Yes

## 5. FAISS Audit
- Index type: FAISS
- Vector dimension: 384
- Total vectors: 39812
- Mapping equality verified: total_vectors (39812) == chunk_count (39812)

## 6 & 7. Retrieval & Generation Audit
Queries were executed against the NQ and HotpotQA sets. The final generations and retrieved context were evaluated. 
Results are stored in `reports/baseline_retrieval_benchmark.csv`.

**Purpose of `baseline_retrieval_benchmark.csv`**:
This file serves as the official clean-system baseline for future adversarial experiments, allowing direct comparison between clean, attacked, and defended states without rerunning baseline experiments.

## 8. Reproducibility Audit
- `README.md` exists.
- `requirements.txt` exists.

## 9. Risks and Issues
- No immediate risks identified. System appears completely functional.

## 10. Recommended Fixes
- None at this time.

## 11. Readiness Score
**READY FOR ATTACK PHASE**
