# Master Figure Inventory & Publication Selection

This document contains a comprehensive audit of all visual artifacts generated across Phases 4A through 6.5 of the RAPTOR project, including candidate rankings and final selection rationale for the 6-page IEEE paper.

---

## 1. Complete Repository Figure Audit

------------------------------------------------
### FIG-01: attack_pipeline_breakdown.png
- **Current Location**: `reports/phase4c/figures/attack_pipeline_breakdown.png`
- **Phase**: Phase 4C
- **Purpose**: Illustrates the breakdown of attack payloads progressing through the retrieval pipeline.
- **Scientific Question Answered**: How do attack payloads degrade across retrieval vs generation stages?
- **Metrics Shown**: Payload Survival Rate, Retrieval Stage Loss, Generation Suppression Rate
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-14 (Sankey Diagram)
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Introduction / Methodology
- **Selection Status**: SELECTED for Paper (Figure 1: figure1_attack_pipeline.png)

------------------------------------------------
### FIG-02: targeted_vs_random_poisoning.png
- **Current Location**: `reports/phase4b_extension/figures/targeted_vs_random_poisoning.png`
- **Phase**: Phase 4B Extension
- **Purpose**: Compares Retrieval Corruption Rate (RCR) between semantic targeted poisoning and naive random insertion.
- **Scientific Question Answered**: Is targeted semantic poisoning significantly more effective than random corpus noise?
- **Metrics Shown**: RCR (%), Attack Ratio (%)
- **Publication Quality**: Yes
- **Redundancy**: Supersedes Phase 4A version
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Threat Model & Attack Evaluation
- **Selection Status**: SELECTED for Paper (Figure 2: figure2_retrieval_poisoning.png)

------------------------------------------------
### FIG-03: asr_by_attack_category.png
- **Current Location**: `reports/phase4c/figures/asr_by_attack_category.png`
- **Phase**: Phase 4C
- **Purpose**: Shows vulnerability profile (ASR) across four distinct attack vectors.
- **Scientific Question Answered**: Which attack category poses the highest empirical threat to RAG systems?
- **Metrics Shown**: ASR (%), RCR (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: High
- **Estimated Paper Section**: Results & Vulnerability Analysis
- **Selection Status**: SELECTED for Paper (Figure 3: figure3_attack_categories.png)

------------------------------------------------
### FIG-04: failure_modes_by_attack.png
- **Current Location**: `reports/phase4f/figures/failure_modes_by_attack.png`
- **Phase**: Phase 4F
- **Purpose**: Categorizes failure modes during generation (Prompt Resistance vs Context Overwrite).
- **Scientific Question Answered**: Why does high retrieval corruption (~99%) not translate into high attack success (~5%)?
- **Metrics Shown**: Failure Mode Breakdown (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: High
- **Estimated Paper Section**: Discussion & Failure Analysis
- **Selection Status**: SELECTED for Paper (Figure 4: figure4_failure_modes.png)

------------------------------------------------
### FIG-05: trust_index_distribution.png
- **Current Location**: `reports/phase6/figures/trust_index_distribution.png`
- **Phase**: Phase 6
- **Purpose**: Displays distribution of Retrieval Trust Index (RTI) scores for clean vs poisoned context chunks.
- **Scientific Question Answered**: Can RTI score effectively separate adversarial chunks from benign context?
- **Metrics Shown**: RTI Score Distribution, Density
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Defense Methodology
- **Selection Status**: SELECTED for Paper (Figure 5: figure5_ragshield_architecture.png)

------------------------------------------------
### FIG-06: asr_before_after.png
- **Current Location**: `reports/phase6/figures/asr_before_after.png`
- **Phase**: Phase 6
- **Purpose**: Compares Attack Success Rate before and after enabling RAGShield across models.
- **Scientific Question Answered**: Does RAGShield effectively mitigate attack success across diverse LLM backbones?
- **Metrics Shown**: ASR Before (%) vs ASR After (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Defense Evaluation
- **Selection Status**: SELECTED for Paper (Figure 6: figure6_defense_evaluation.png)

------------------------------------------------
### FIG-07: security_vs_utility_pareto.png
- **Current Location**: `reports/phase6_5/optimization/figures/security_vs_utility_pareto.png`
- **Phase**: Phase 6.5
- **Purpose**: Plots the Pareto frontier of Security (ASR reduction) versus Utility (Clean QA containment).
- **Scientific Question Answered**: What is the optimal operational threshold balancing security defense and QA utility?
- **Metrics Shown**: ASR (%), Containment Utility (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: High
- **Estimated Paper Section**: Adaptive Optimization & Tradeoffs
- **Selection Status**: SELECTED for Paper (Figure 7: figure7_security_utility_pareto.png)

------------------------------------------------
### FIG-08: rcr_vs_attack_ratio.png
- **Current Location**: `reports/phase4b_extension/figures/rcr_vs_attack_ratio.png`
- **Phase**: Phase 4B Extension
- **Purpose**: Measures Retrieval Corruption Rate scaling with poison density.
- **Scientific Question Answered**: How quickly does RCR saturate as poison ratio increases?
- **Metrics Shown**: RCR (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-02
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Threat Model
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-09: asr_vs_attack_ratio.png
- **Current Location**: `reports/phase4b_extension/figures/asr_vs_attack_ratio.png`
- **Phase**: Phase 4B Extension
- **Purpose**: Measures Attack Success Rate scaling with poison density.
- **Scientific Question Answered**: Does higher poison ratio linearly increase LLM attack success?
- **Metrics Shown**: ASR (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-02
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Threat Model
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-10: targeted_vs_untargeted_asr.png
- **Current Location**: `reports/phase4b_extension/figures/targeted_vs_untargeted_asr.png`
- **Phase**: Phase 4B Extension
- **Purpose**: Compares targeted ASR against untargeted injection ASR.
- **Scientific Question Answered**: Is targeted injection more successful than generic prompt hijacking?
- **Metrics Shown**: Targeted ASR vs Untargeted ASR (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-03
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Threat Model
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-11: targeted_vs_untargeted_rcr.png
- **Current Location**: `reports/phase4b_extension/figures/targeted_vs_untargeted_rcr.png`
- **Phase**: Phase 4B Extension
- **Purpose**: Compares targeted RCR against untargeted injection RCR.
- **Scientific Question Answered**: Does targeted poisoning achieve higher retrieval penetration?
- **Metrics Shown**: Targeted RCR vs Untargeted RCR (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-02
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Threat Model
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-12: attack_category_comparison.png
- **Current Location**: `reports/phase4c/figures/attack_category_comparison.png`
- **Phase**: Phase 4C
- **Purpose**: Multi-axis comparison of 4 attack categories.
- **Scientific Question Answered**: How do attack categories compare in terms of latency, RCR, and ASR?
- **Metrics Shown**: RCR, ASR, Latency
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-03
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Results
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-13: rcr_by_attack_category.png
- **Current Location**: `reports/phase4c/figures/rcr_by_attack_category.png`
- **Phase**: Phase 4C
- **Purpose**: Retrieval corruption rate per attack category.
- **Scientific Question Answered**: Which attack category penetrates FAISS retrieval most effectively?
- **Metrics Shown**: RCR (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-03
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Results
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-14: attack_pipeline_sankey.png
- **Current Location**: `reports/phase4f/figures/attack_pipeline_sankey.png`
- **Phase**: Phase 4F
- **Purpose**: Sankey flow diagram of query progression from corpus to final output.
- **Scientific Question Answered**: Where are attack payloads lost in the pipeline flow?
- **Metrics Shown**: Flow counts (queries)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-01
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Discussion
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-15: failure_modes_by_model.png
- **Current Location**: `reports/phase4f/figures/failure_modes_by_model.png`
- **Phase**: Phase 4F
- **Purpose**: Failure mode distribution across Mistral, Qwen2.5, and Llama3.1.
- **Scientific Question Answered**: Do different LLM backbones exhibit distinct prompt resistance behaviors?
- **Metrics Shown**: Failure Mode % by Model
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-04
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Discussion
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-16: model_vs_attack_heatmap.png
- **Current Location**: `reports/phase6/baseline/figures/model_vs_attack_heatmap.png`
- **Phase**: Phase 6 Baseline
- **Purpose**: Heatmap of model performance across attack vectors.
- **Scientific Question Answered**: Which model-attack pairs represent the highest vulnerability matrix?
- **Metrics Shown**: ASR (%) Heatmap
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Model Sensitivity
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-17: rcr_before_after.png
- **Current Location**: `reports/phase6/figures/rcr_before_after.png`
- **Phase**: Phase 6
- **Purpose**: Compares RCR before and after RAGShield.
- **Scientific Question Answered**: Does RAGShield reduce retrieval corruption?
- **Metrics Shown**: RCR Before vs After (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-06
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Defense Evaluation
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-18: threshold_vs_rates.png
- **Current Location**: `reports/phase6_5/optimization/figures/threshold_vs_rates.png`
- **Phase**: Phase 6.5
- **Purpose**: Plots threshold sensitivity vs RCR and False Positive Rate (FPR).
- **Scientific Question Answered**: How does minimum RTI score impact false positive rate?
- **Metrics Shown**: RCR (%), FPR (%)
- **Publication Quality**: Yes
- **Redundancy**: Similar to FIG-07
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Optimization
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-19: trust_weight_heatmap.png
- **Current Location**: `reports/phase6_5/optimization/figures/trust_weight_heatmap.png`
- **Phase**: Phase 6.5
- **Purpose**: Heatmap of Optimization Scores across alpha/beta/gamma weight grid.
- **Scientific Question Answered**: What weight balance maximizes the Retrieval Trust Index performance?
- **Metrics Shown**: Optimization Score Heatmap
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary / Optimization
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-20: accuracy_by_corpus.png
- **Current Location**: `reports/phase4d/figures/accuracy_by_corpus.png`
- **Phase**: Phase 4D
- **Purpose**: Clean QA Accuracy across evaluation corpora.
- **Scientific Question Answered**: Does poisoning corrupt clean query answers?
- **Metrics Shown**: Accuracy (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Low
- **Estimated Paper Section**: Supplementary / Utility Impact
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-21: attack_vs_accuracy_tradeoff.png
- **Current Location**: `reports/phase4d/figures/attack_vs_accuracy_tradeoff.png`
- **Phase**: Phase 4D
- **Purpose**: Tradeoff curve between attack success and QA accuracy degradation.
- **Scientific Question Answered**: Is QA accuracy inversely proportional to attack success?
- **Metrics Shown**: Accuracy (%) vs ASR (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Low
- **Estimated Paper Section**: Supplementary / Utility Impact
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### FIG-22: containment_accuracy_by_corpus.png
- **Current Location**: `reports/phase4d_reanalysis/figures/containment_accuracy_by_corpus.png`
- **Phase**: Phase 4D Reanalysis
- **Purpose**: Containment-based accuracy reanalysis across corpora.
- **Scientific Question Answered**: How does exact containment metric compare to EM/F1 for QA evaluation?
- **Metrics Shown**: Containment Accuracy (%)
- **Publication Quality**: Yes
- **Redundancy**: None
- **Recommended Priority**: Low
- **Estimated Paper Section**: Supplementary / Reanalysis
- **Selection Status**: Excluded (Moved to Supplementary)

---

## 2. Top 15 Figures (Ranked by Scientific Rationale)

| Rank | Figure ID | Filename | Phase | Scientific Importance & Reviewer Value | Selection |
|---|---|---|---|---|---|
| **1** | FIG-01 | `attack_pipeline_breakdown.png` | Phase 4C | **Critical**: Defines the core threat model and shows end-to-end payload degradation across retrieval vs generation. Essential for introducing the paper's domain. | Selected (Fig 1) |
| **2** | FIG-05 | `trust_index_distribution.png` | Phase 6 | **Critical**: Introduces the novel Retrieval Trust Index (RTI) density distribution separating clean from poisoned chunks. Core architectural novelty. | Selected (Fig 5) |
| **3** | FIG-06 | `asr_before_after.png` | Phase 6 | **Critical**: Directly answers whether RAGShield works by comparing Attack Success Rate (ASR) before and after defense across all 3 models. Key result. | Selected (Fig 6) |
| **4** | FIG-02 | `targeted_vs_random_poisoning.png` | Phase 4B Ext | **Critical**: Proves empirically that semantic targeted poisoning (~99% RCR) far outpaces random noise. Primary threat validation. | Selected (Fig 2) |
| **5** | FIG-03 | `asr_by_attack_category.png` | Phase 4C | **High**: Compares vulnerability across all 4 attack vectors (KP, II, GH, IE). Demonstrates comprehensive vulnerability profiling. | Selected (Fig 3) |
| **6** | FIG-04 | `failure_modes_by_attack.png` | Phase 4F | **High**: Solves the central mystery of why high retrieval corruption (~99%) yields low ASR (~5%) due to LLM prompt resistance. | Selected (Fig 4) |
| **7** | FIG-07 | `security_vs_utility_pareto.png` | Phase 6.5 | **High**: Shows the Pareto frontier between ASR defense and QA Containment utility across threshold configurations. Essential for systems paper. | Selected (Fig 7) |
| **8** | FIG-19 | `trust_weight_heatmap.png` | Phase 6.5 | **Medium**: Grid search heatmap for alpha/beta/gamma weights. Valuable for tuning analysis but secondary to Pareto plot. | Excluded |
| **9** | FIG-16 | `model_vs_attack_heatmap.png` | Phase 6 Base | **Medium**: Multi-model vulnerability matrix heatmap. Highly informative but captured in main tables. | Excluded |
| **10** | FIG-14 | `attack_pipeline_sankey.png` | Phase 4F | **Medium**: Beautiful Sankey flow diagram of query progression, but redundant with FIG-01 flow diagram. | Excluded |
| **11** | FIG-18 | `threshold_vs_rates.png` | Phase 6.5 | **Medium**: Sensitivity curve for minimum RTI threshold vs FPR. Redundant with Pareto frontier curve (FIG-07). | Excluded |
| **12** | FIG-15 | `failure_modes_by_model.png` | Phase 4F | **Medium**: Model-specific failure modes. Redundant with attack-specific failure breakdown (FIG-04). | Excluded |
| **13** | FIG-17 | `rcr_before_after.png` | Phase 6 | **Medium**: RCR before/after defense. Superseded by overall ASR before/after plot (FIG-06). | Excluded |
| **14** | FIG-12 | `attack_category_comparison.png` | Phase 4C | **Medium**: Multi-axis category comparison. Superseded by FIG-03 bar plot. | Excluded |
| **15** | FIG-08 | `rcr_vs_attack_ratio.png` | Phase 4B Ext | **Medium**: RCR scaling curve. Information contained in FIG-02 comparison plot. | Excluded |

---

## 3. Final IEEE Figures Selection Summary (Target: 7 Figures)

1. **Figure 1**: `figure1_attack_pipeline.png` (Section: Introduction / Threat Model)
   - *Reason for inclusion*: Establishes threat model and end-to-end RAG poisoning lifecycle.
   - *Reason for exclusions*: Replaced alternative Sankey diagram (FIG-14) for clearer 2-column layout fit.
2. **Figure 2**: `figure2_retrieval_poisoning.png` (Section: Threat Model & Attack Evaluation)
   - *Reason for inclusion*: Proves retrieval-aware semantic targeting achieves ~99% RCR vs random noise.
   - *Reason for exclusions*: Supersedes earlier Phase 4A scaling plots (FIG-08, FIG-09).
3. **Figure 3**: `figure3_attack_categories.png` (Section: Results & Vulnerability Analysis)
   - *Reason for inclusion*: Comprehensive vulnerability baseline across 4 attack categories.
   - *Reason for exclusions*: Replaces individual category breakdowns (FIG-12, FIG-13).
4. **Figure 4**: `figure4_failure_modes.png` (Section: Discussion & Failure Analysis)
   - *Reason for inclusion*: Explains prompt resistance bottleneck preventing RCR from becoming ASR.
   - *Reason for exclusions*: Chosen over per-model plot (FIG-15) as attack vector is primary variable.
5. **Figure 5**: `figure5_ragshield_architecture.png` (Section: Defense Methodology)
   - *Reason for inclusion*: Demonstrates RTI score separation between clean and poisoned chunks.
   - *Reason for exclusions*: Only plot explicitly showing chunk-level density separation.
6. **Figure 6**: `figure6_defense_evaluation.png` (Section: Defense Evaluation)
   - *Reason for inclusion*: Primary quantitative result showing ASR mitigation across all 3 models.
   - *Reason for exclusions*: Supersedes separate RCR before/after plot (FIG-17).
7. **Figure 7**: `figure7_security_utility_pareto.png` (Section: Adaptive Optimization & Tradeoffs)
   - *Reason for inclusion*: Demonstrates Pareto security-utility trade-off curve across operational thresholds.
   - *Reason for exclusions*: Combines information from 2D sensitivity curves (FIG-18) and weight heatmaps (FIG-19).
