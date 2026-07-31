# Phase 4D.2: Accuracy Re-Scoring Audit

## Overview
A lightweight re-evaluation of 100 randomly sampled questions across all 5 corpora was conducted to determine the true QA accuracy using Answer Containment Accuracy.

## Impact of Metric Choice
When using traditional Exact Match (EM) and F1 scores, Mistral's verbose conversational generation penalizes the performance. The Clean baseline achieved an EM of 0.0000 and F1 of 0.0190. However, the Answer Containment Accuracy, which normalizes strings and checks for ground-truth presence, revealed a true accuracy of 0.6400 (or 64.0%).

## Poisoned vs Clean Containment
- **Knowledge Poisoning**: 0.6300 (-0.0100 absolute change, -1.56% relative degradation).
- **Instruction Injection**: 0.6300 (-0.0100 absolute change, -1.56% relative degradation).
- **Goal Hijacking**: 0.6200 (-0.0200 absolute change, -3.13% relative degradation).
- **Information Extraction**: 0.6400 (0.0000 absolute change, 0.00% relative degradation).

## Conclusion
The Answer Containment Accuracy metric confirms that despite the attacks successfully retrieving poisoned chunks, the material degradation in factual correctness varies by attack type compared to the Clean baseline.
