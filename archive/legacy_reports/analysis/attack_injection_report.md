# Attack Injection Report (Phase 3B)

## 1. Executive Summary
This report documents the successful implementation of the controlled attack injection pipeline for the RAPTOR project. A diverse attack corpus was procedurally generated from the core BIPIA prompts, and these were randomly injected into the clean Wikipedia knowledge base at configurable ratios.

## 2. Attack Categories Used
The benchmark was built using the 4 prioritized categories to ensure a mix of direct payload injections and filter-evading obfuscations:
- **Malware Distribution** (Payload)
- **Clickbait** (Payload)
- **Persuasion** (Payload)
- **Alphanumeric Substitution** (Obfuscation)

## 3. Attack Corpus Generation
To maximize attack diversity and prevent overfitting to a small sample of exact prompts, an expanded attack corpus was procedurally generated.
- **Base Prompts Used**: 20 (5 per category)
- **Total Generated Attack Documents**: 1,000 (250 per category)
- **Generation Strategy**: The original BIPIA prompts were paraphrased using synonym replacement and embedded within contextual wrappers to simulate realistic document structures (e.g., historical contexts, headers, lists).

## 4. Injection Pipeline Ratios
The attack documents were randomly injected (with replacement) into the clean dataset. 

| Metric | Count / Size |
|---|---|
| **Clean Dataset Size** | 39,812 chunks |
| **1% Attack Ratio** | 398 injected attacks |
| **5% Attack Ratio** | 1,990 injected attacks |
| **10% Attack Ratio** | 3,981 injected attacks |

### Final Poisoned Dataset Sizes
- **1% Poisoned Set**: 40,210 chunks (`data/processed/wikipedia_chunks_attacked_1pct`)
- **5% Poisoned Set**: 41,802 chunks (`data/processed/wikipedia_chunks_attacked_5pct`)
- **10% Poisoned Set**: 43,793 chunks (`data/processed/wikipedia_chunks_attacked_10pct`)

## 5. Validation Summary
- **Original Dataset Unchanged**: The clean `data/processed/wikipedia_chunks` dataset was preserved.
- **Attack Chunk Counts Match Ratio**: The mathematical addition of attacks perfectly aligns with the generated file sizes.
- **No Duplicate Chunk IDs**: The pipeline explicitly formats injected `chunk_id` fields dynamically to ensure global uniqueness within the knowledge base.

*The RAPTOR RAG system now has multiple validated, poisoned knowledge bases ready for the adversarial testing phase.*
