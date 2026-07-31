# Phase 6.5 Adaptive RTI Optimization Summary

## Recommended Configuration
- **Best RTI Weights**: alpha=0.30, beta=0.50, gamma=0.20
- **Best Threshold**: 0.25
- **Consistency Penalty Weight**: 0.5 (Fixed for this run)

## Optimization Results (Mistral Knowledge Poisoning)
- **Retrieval Corruption Rate (RCR)**: 100.0%
- **Attack Success Rate (ASR)**: 4.0%
- **Utility Preservation (Containment)**: 45.0%

## Key Findings
Despite sweeping across all combinations of trust weights, thresholds, and introducing a Consistency Penalty and Hard Trust Filtering, the RCR remained stubbornly at 100%. This implies that Knowledge Poisoning attacks are structurally and semantically indistinguishable from valid chunks under the current semantic models, overpowering both the consensus analyzer and the base retrieval confidence.
