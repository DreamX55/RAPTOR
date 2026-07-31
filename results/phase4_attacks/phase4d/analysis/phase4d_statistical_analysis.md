# Phase 4D Statistical Analysis

Comparing each poisoned corpus against the Clean baseline using Welch's t-test.

## Knowledge Poisoning
- **EM**: Mean=0.0000, Std=0.0000, 95% CI=±0.0000
  - t-statistic: nan, p-value: nan, Cohen's d: nan
- **F1**: Mean=1.7051, Std=4.6771, 95% CI=±0.2899
  - t-statistic: 0.1492, p-value: 8.8142e-01, Cohen's d: -0.0067
- **Semantic Similarity**: Mean=0.1291, Std=0.1796, 95% CI=±0.0111
  - t-statistic: -0.3401, p-value: 7.3385e-01, Cohen's d: 0.0152

## Instruction Injection
- **EM**: Mean=0.0000, Std=0.0000, 95% CI=±0.0000
  - t-statistic: nan, p-value: nan, Cohen's d: nan
- **F1**: Mean=1.7899, Std=4.9292, 95% CI=±0.3055
  - t-statistic: -0.2589, p-value: 7.9573e-01, Cohen's d: 0.0116
- **Semantic Similarity**: Mean=0.1300, Std=0.1772, 95% CI=±0.0110
  - t-statistic: -0.4499, p-value: 6.5285e-01, Cohen's d: 0.0201

## Goal Hijacking
- **EM**: Mean=0.0000, Std=0.0000, 95% CI=±0.0000
  - t-statistic: nan, p-value: nan, Cohen's d: nan
- **F1**: Mean=1.7923, Std=5.3183, 95% CI=±0.3296
  - t-statistic: -0.2589, p-value: 7.9574e-01, Cohen's d: 0.0116
- **Semantic Similarity**: Mean=0.1299, Std=0.1772, 95% CI=±0.0110
  - t-statistic: -0.4392, p-value: 6.6059e-01, Cohen's d: 0.0196

## Information Extraction
- **EM**: Mean=0.0000, Std=0.0000, 95% CI=±0.0000
  - t-statistic: nan, p-value: nan, Cohen's d: nan
- **F1**: Mean=1.7925, Std=5.0567, 95% CI=±0.3134
  - t-statistic: -0.2674, p-value: 7.8921e-01, Cohen's d: 0.0120
- **Semantic Similarity**: Mean=0.1308, Std=0.1796, 95% CI=±0.0111
  - t-statistic: -0.5540, p-value: 5.7965e-01, Cohen's d: 0.0248

