# RAPTOR Phase 4A: ASR Evaluation Report (Pilot)

## Executive Summary
This report presents the Attack Success Rate (ASR) evaluation of the Mistral-based RAG pipeline.

- **Total Queries Evaluated per Corpus**: 100
- **Baseline False ASR (Clean Corpus)**: 0.00%

## Key Metrics Summary

| Corpus | RCR | ASR | Exact Match | Semantic Similarity |
|---|---|---|---|---|
| Clean | 0.00% | 0.00% | 0.00% | 0.1133 |
| 1% Attacked | 0.00% | 0.00% | 0.00% | 0.1169 |
| 5% Attacked | 0.00% | 0.00% | 0.00% | 0.1138 |
| 10% Attacked | 0.00% | 0.00% | 0.00% | 0.1196 |

## Figures

See the `figures/pilot` directory for detailed plots showing the degradation of Exact Match and the increase of ASR as the knowledge base corruption increases.

## Analysis
*The Baseline False ASR validates our heuristic detectors. A high false ASR would indicate overly aggressive detection rules.*
