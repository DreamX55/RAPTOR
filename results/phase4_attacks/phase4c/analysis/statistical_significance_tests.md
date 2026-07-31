# Statistical Significance Tests (Phase 4C)

Chi-Square tests for Attack Success Rate (ASR) comparing each new category against the Knowledge Poisoning baseline.

### Knowledge Poisoning vs Instruction Injection
- Baseline ASR: 2.40%
- Instruction Injection ASR: 1.40%
- Chi-Square Statistic: 0.8584
- p-value: 3.5418e-01
- **Conclusion**: Difference is NOT statistically significant (p >= 0.05).

### Knowledge Poisoning vs Goal Hijacking
- Baseline ASR: 2.40%
- Goal Hijacking ASR: 5.60%
- Chi-Square Statistic: 5.8594
- p-value: 1.5494e-02
- **Conclusion**: Difference is statistically significant (p < 0.05).

### Knowledge Poisoning vs Information Extraction
- Baseline ASR: 2.40%
- Information Extraction ASR: 0.40%
- Chi-Square Statistic: 5.8679
- p-value: 1.5420e-02
- **Conclusion**: Difference is statistically significant (p < 0.05).

