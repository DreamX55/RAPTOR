# Master Table Inventory & Publication Selection

This document contains a comprehensive audit of all tables generated across Phases 4A through 6.5 of the RAPTOR project, including selection rationale for the 6-page IEEE paper.

---

## 1. Complete Repository Table Audit

------------------------------------------------
### TBL-01: Table_1_Attack_Configuration_Summary.md
- **Current Location**: `reports/phase4b_extension/tables/Table_1_Attack_Configuration_Summary.md`
- **Phase**: Phase 4B Extension
- **Purpose**: Summarizes the dataset sizes, chunk counts, attack types, and corpus configurations.
- **Metrics Shown**: Corpus Name, Total Chunks, Poison Ratio, Attack Vector
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Experimental Setup
- **Selection Status**: SELECTED for Paper (Table 1: table1_attack_summary.md)

------------------------------------------------
### TBL-02: Table_All_Categories_Comparison.md
- **Current Location**: `reports/phase4c/tables/Table_All_Categories_Comparison.md`
- **Phase**: Phase 4C
- **Purpose**: Comparative security performance across Knowledge Poisoning, Instruction Injection, Goal Hijacking, and Information Extraction.
- **Metrics Shown**: RCR (%), ASR (%), Latency Overhead (ms)
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Results & Vulnerability Analysis
- **Selection Status**: SELECTED for Paper (Table 2: table2_category_comparison.md)

------------------------------------------------
### TBL-03: Table_1_Overall_QA_Performance.md
- **Current Location**: `reports/phase4d/tables/Table_1_Overall_QA_Performance.md`
- **Phase**: Phase 4D
- **Purpose**: Evaluates baseline QA performance across Mistral, Qwen2.5:7b, and Llama3.1:8b backbones.
- **Metrics Shown**: Exact Match (EM), F1-Score, Containment Accuracy (%)
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Model Sensitivity Analysis
- **Selection Status**: SELECTED for Paper (Table 3: table3_multimodel_eval.md)

------------------------------------------------
### TBL-04: Optimization_Summary.md
- **Current Location**: `reports/phase6_5/optimization/analysis/Optimization_Summary.md`
- **Phase**: Phase 6.5
- **Purpose**: Summarizes RAGShield defense performance, RCR mitigation, ASR drop, and containment utility.
- **Metrics Shown**: RCR (%), ASR (%), Containment Utility (%), Latency (ms)
- **Recommended Priority**: Critical
- **Estimated Paper Section**: Defense Evaluation
- **Selection Status**: SELECTED for Paper (Table 4: table4_ragshield_performance.md)

------------------------------------------------
### TBL-05: Weight_Search_Results.md
- **Current Location**: `reports/phase6_5/optimization/analysis/Weight_Search_Results.md`
- **Phase**: Phase 6.5
- **Purpose**: Details Stage 1 offline grid search results for RTI weight parameter optimization.
- **Metrics Shown**: Alpha, Beta, Gamma, Threshold, RCR (%), FPR (%), Optimization Score
- **Recommended Priority**: High
- **Estimated Paper Section**: Optimization & Hyperparameter Search
- **Selection Status**: SELECTED for Paper (Table 5: table5_optimization_results.md)

------------------------------------------------
### TBL-06: Table_3_System_Resource_Utilization.md
- **Current Location**: `reports/phase4b_extension/tables/Table_3_System_Resource_Utilization.md`
- **Phase**: Phase 4B Extension
- **Purpose**: Measures memory footprint (VRAM/RAM) and microsecond latency per component.
- **Metrics Shown**: RAM (MB), VRAM (MB), Retrieval Latency (ms), Scorer Latency (ms)
- **Recommended Priority**: High
- **Estimated Paper Section**: System Efficiency & Overhead
- **Selection Status**: SELECTED for Paper (Table 6: table6_system_overhead.md)

------------------------------------------------
### TBL-07: Table_KP_vs_Instruction_Injection.md
- **Current Location**: `reports/phase4c/tables/Table_KP_vs_Instruction_Injection.md`
- **Phase**: Phase 4C
- **Purpose**: Direct head-to-head metrics for Knowledge Poisoning vs Instruction Injection.
- **Metrics Shown**: Delta RCR (%), Delta ASR (%)
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### TBL-08: Table_KP_vs_Goal_Hijacking.md
- **Current Location**: `reports/phase4c/tables/Table_KP_vs_Goal_Hijacking.md`
- **Phase**: Phase 4C
- **Purpose**: Head-to-head metrics for Knowledge Poisoning vs Goal Hijacking.
- **Metrics Shown**: Delta RCR (%), Delta ASR (%)
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### TBL-09: Table_KP_vs_Information_Extraction.md
- **Current Location**: `reports/phase4c/tables/Table_KP_vs_Information_Extraction.md`
- **Phase**: Phase 4C
- **Purpose**: Head-to-head metrics for Knowledge Poisoning vs Information Extraction.
- **Metrics Shown**: Delta RCR (%), Delta ASR (%)
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### TBL-10: transition_table.md
- **Current Location**: `reports/phase4f/tables/transition_table.md`
- **Phase**: Phase 4F
- **Purpose**: State transition counts from Retrieval to Generation stages.
- **Metrics Shown**: Transition probabilities, Query counts
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### TBL-11: Table_2_Relative_Accuracy_Degradation.md
- **Current Location**: `reports/phase4d/tables/Table_2_Relative_Accuracy_Degradation.md`
- **Phase**: Phase 4D
- **Purpose**: Measures relative degradation in QA accuracy due to adversarial presence.
- **Metrics Shown**: Relative Accuracy Drop (%)
- **Recommended Priority**: Medium
- **Estimated Paper Section**: Supplementary
- **Selection Status**: Excluded (Moved to Supplementary)

------------------------------------------------
### TBL-12: Table_3_Dataset_Breakdown.md
- **Current Location**: `reports/phase4d/tables/Table_3_Dataset_Breakdown.md`
- **Phase**: Phase 4D
- **Purpose**: Breakdown of benchmark dataset questions and ground truth lengths.
- **Metrics Shown**: Question Count, Avg Word Length
- **Recommended Priority**: Low
- **Estimated Paper Section**: Supplementary
- **Selection Status**: Excluded (Moved to Supplementary)

---

## 2. Top Tables (Ranked by Scientific Rationale)

| Rank | Table ID | Filename | Phase | Scientific Importance & Reviewer Value | Selection |
|---|---|---|---|---|---|
| **1** | TBL-01 | `Table_1_Attack_Configuration_Summary.md` | Phase 4B Ext | **Critical**: Defines dataset corpora, chunk counts, and poison ratios. Mandatory experimental baseline. | Selected (Table 1) |
| **2** | TBL-02 | `Table_All_Categories_Comparison.md` | Phase 4C | **Critical**: Main benchmark results across all 4 attack categories showing RCR, ASR, and latencies. | Selected (Table 2) |
| **3** | TBL-03 | `Table_1_Overall_QA_Performance.md` | Phase 4D | **Critical**: Baseline multi-LLM benchmark evaluation across Mistral, Qwen2.5, and Llama3.1. | Selected (Table 3) |
| **4** | TBL-04 | `Optimization_Summary.md` | Phase 6.5 | **Critical**: Evaluates RAGShield defense performance, ASR reduction, and Containment utility. | Selected (Table 4) |
| **5** | TBL-05 | `Weight_Search_Results.md` | Phase 6.5 | **High**: Details Stage 1 offline grid search for RTI hyperparameter optimization. | Selected (Table 5) |
| **6** | TBL-06 | `Table_3_System_Resource_Utilization.md` | Phase 4B Ext | **High**: System efficiency table detailing microsecond latency and VRAM/RAM memory overhead. | Selected (Table 6) |

---

## 3. Final IEEE Tables Selection Summary (Target: 6 Tables)

1. **Table 1**: `table1_attack_summary.md` (Section: Experimental Setup)
2. **Table 2**: `table2_category_comparison.md` (Section: Results & Vulnerability Analysis)
3. **Table 3**: `table3_multimodel_eval.md` (Section: Model Sensitivity Analysis)
4. **Table 4**: `table4_ragshield_performance.md` (Section: Defense Evaluation)
5. **Table 5**: `table5_optimization_results.md` (Section: Optimization & Hyperparameter Search)
6. **Table 6**: `table6_system_overhead.md` (Section: System Efficiency & Overhead)
