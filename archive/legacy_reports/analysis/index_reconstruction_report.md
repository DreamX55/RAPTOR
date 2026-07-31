# Index Reconstruction Report

## Overview
This report verifies the successful regeneration of the clean and attacked FAISS indexes against the expanded >100k chunk corpus.

## Base Clean Corpus
- **Dataset Size**: 106,463 chunks
- **FAISS Vectors**: 106,463
- **Dimension**: 384
- **Status**: Passed

## Attacked Corpora

| Attack Ratio | Target Dataset | Expected Chunks | FAISS Vectors | Status |
|---|---|---|---|---|
| 1% | `_attacked_1pct` | 107,527 | 107,527 | Passed |
| 5% | `_attacked_5pct` | 111,786 | 111,786 | Passed |
| 10% | `_attacked_10pct` | 117,109 | 117,109 | Passed |

## Summary
Overall Validation: **SUCCESS**

The retrieval infrastructure has been successfully rebuilt and dimensionally verified. The system is fully ready for the ASR evaluation benchmark.
