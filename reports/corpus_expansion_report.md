# Corpus Expansion Report (Phase 3C)

## 1. Executive Summary
This report details the successful expansion of the RAPTOR retrieval corpus. The primary objective was to expand the clean Wikipedia knowledge base to exceed 100,000 retrievable chunks, providing a more robust and realistic environment for subsequent adversarial RAG experiments.

## 2. Corpus Size and Growth
To achieve the requirement of >100,000 chunks, the acquisition target was dynamically scaled from 5,000 articles up to 30,000 articles. The datasets were deliberately saved as `wikipedia_15k` as requested, keeping the legacy 5k datasets fully intact for baseline preservation.

| Metric | Original Baseline | Expanded Corpus (`_15k`) |
|---|---|---|
| **Article Count** | 5,000 | 30,000 |
| **Chunk Count** | 39,812 | 106,463 |
| **Average Chunk Size** | ~54 words | ~54 words |

*(Note: While the directory is named `15k`, 30,000 articles were safely downloaded to guarantee the chunks exceeded 100,000 based on the empirical average of ~3.5 chunks per article).*

## 3. Storage and Reproducibility
- The expanded raw dataset is saved at `data/raw/wikipedia_15k`.
- The expanded semantic chunks are saved at `data/processed/wikipedia_chunks_15k`.
- The original `data/raw/wikipedia` and `data/processed/wikipedia_chunks` (5k baseline) remain completely untouched.

> [!WARNING]
> **Regeneration Required**
> Because the underlying clean corpus size has fundamentally changed (from ~40k chunks to ~106k chunks), all previously generated **attacked datasets** (Phase 3B) and **attacked FAISS indexes** will need to be regenerated against this new, expanded baseline before evaluating the adversarial attacks.

## 4. Future Evaluation Benchmark Specification
To prepare for the upcoming Attack Success Rate (ASR) experiments, we have established the following evaluation benchmark specification:
- **1,000 Natural Questions** (NQ)
- **1,000 HotpotQA Questions**
- **Total Evaluation Set**: 2,000 questions

This evaluation set provides a statistically significant testing ground to evaluate exactly how effectively the injected BIPIA attacks hijack the generation phase under load.
