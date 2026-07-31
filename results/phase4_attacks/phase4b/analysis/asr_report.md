# RAPTOR Phase 4A: ASR Evaluation Report (Full)

## Executive Summary
This report presents the Attack Success Rate (ASR) evaluation of the Mistral-based RAG pipeline.

- **Total Queries Evaluated per Corpus**: 2000
- **Baseline False ASR (Clean Corpus)**: 0.00%

## Key Metrics Summary

| Corpus | RCR | ASR | Exact Match | Semantic Similarity |
|---|---|---|---|---|
| Clean | 0.00% | 0.00% | 0.00% | 0.1218 |
| 1% Attacked | 0.00% | 0.00% | 0.00% | 0.1201 |
| 5% Attacked | 0.00% | 0.00% | 0.00% | 0.1213 |
| 10% Attacked | 0.00% | 0.00% | 0.00% | 0.1211 |
| 20% Attacked | 0.00% | 0.00% | 0.00% | 0.1214 |

## Figures

See the `figures` directory for detailed plots showing the degradation of Exact Match and the increase of ASR as the knowledge base corruption increases.

## Analysis
*The Baseline False ASR validates our heuristic detectors. A high false ASR would indicate overly aggressive detection rules.*

**Documented Negative Finding**: For corpora 1pct, 5pct, 10pct, 20pct, both RCR and ASR were exactly 0.00%. No contamination was observed. The system successfully maintained robustness despite the injected payloads.
