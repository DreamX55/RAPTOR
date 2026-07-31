import os
import shutil

REPORTS_DIR = "reports"
PAPER_ASSETS_DIR = os.path.join(REPORTS_DIR, "paper_assets")
PAPER_DIR = "paper"
PAPER_FIGS_DIR = os.path.join(PAPER_DIR, "figures")
PAPER_TBLS_DIR = os.path.join(PAPER_DIR, "tables")

os.makedirs(PAPER_ASSETS_DIR, exist_ok=True)
os.makedirs(PAPER_FIGS_DIR, exist_ok=True)
os.makedirs(PAPER_TBLS_DIR, exist_ok=True)

# 1. Figure Inventory Data
figures_data = [
    {
        "id": "FIG-01",
        "filename": "attack_pipeline_breakdown.png",
        "location": "reports/phase4c/figures/attack_pipeline_breakdown.png",
        "phase": "Phase 4C",
        "purpose": "Illustrates the breakdown of attack payloads progressing through the retrieval pipeline.",
        "question": "How do attack payloads degrade across retrieval vs generation stages?",
        "metrics": "Payload Survival Rate, Retrieval Stage Loss, Generation Suppression Rate",
        "quality": "Yes",
        "redundancy": "Similar to FIG-14 (Sankey Diagram)",
        "priority": "Critical",
        "section": "Introduction / Methodology",
        "selected_for_paper": True,
        "new_name": "figure1_attack_pipeline.png",
        "paper_num": "Figure 1",
        "caption": "End-to-End Poisoning Flow and Information Degradation across the RAG Retrieval-Generation Lifecycle."
    },
    {
        "id": "FIG-02",
        "filename": "targeted_vs_random_poisoning.png",
        "location": "reports/phase4b_extension/figures/targeted_vs_random_poisoning.png",
        "phase": "Phase 4B Extension",
        "purpose": "Compares Retrieval Corruption Rate (RCR) between semantic targeted poisoning and naive random insertion.",
        "question": "Is targeted semantic poisoning significantly more effective than random corpus noise?",
        "metrics": "RCR (%), Attack Ratio (%)",
        "quality": "Yes",
        "redundancy": "Supersedes Phase 4A version",
        "priority": "Critical",
        "section": "Threat Model & Attack Evaluation",
        "selected_for_paper": True,
        "new_name": "figure2_retrieval_poisoning.png",
        "paper_num": "Figure 2",
        "caption": "Retrieval Corruption Rate (RCR) and Attack Success Rate (ASR) Comparison Between Targeted Retrieval-Aware Poisoning and Random Poisoning."
    },
    {
        "id": "FIG-03",
        "filename": "asr_by_attack_category.png",
        "location": "reports/phase4c/figures/asr_by_attack_category.png",
        "phase": "Phase 4C",
        "purpose": "Shows vulnerability profile (ASR) across four distinct attack vectors.",
        "question": "Which attack category poses the highest empirical threat to RAG systems?",
        "metrics": "ASR (%), RCR (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "High",
        "section": "Results & Vulnerability Analysis",
        "selected_for_paper": True,
        "new_name": "figure3_attack_categories.png",
        "paper_num": "Figure 3",
        "caption": "Vulnerability Profile and Attack Success Rate Across Diverse Injection Tactics (Knowledge Poisoning, Instruction Injection, Goal Hijacking, Information Extraction)."
    },
    {
        "id": "FIG-04",
        "filename": "failure_modes_by_attack.png",
        "location": "reports/phase4f/figures/failure_modes_by_attack.png",
        "phase": "Phase 4F",
        "purpose": "Categorizes failure modes during generation (Prompt Resistance vs Context Overwrite).",
        "question": "Why does high retrieval corruption (~99%) not translate into high attack success (~5%)?",
        "metrics": "Failure Mode Breakdown (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "High",
        "section": "Discussion & Failure Analysis",
        "selected_for_paper": True,
        "new_name": "figure4_failure_modes.png",
        "paper_num": "Figure 4",
        "caption": "Categorical Breakdown of Pipeline Bottlenecks and Failure Modes Indicating Prompt Resistance during Generation."
    },
    {
        "id": "FIG-05",
        "filename": "trust_index_distribution.png",
        "location": "reports/phase6/figures/trust_index_distribution.png",
        "phase": "Phase 6",
        "purpose": "Displays distribution of Retrieval Trust Index (RTI) scores for clean vs poisoned context chunks.",
        "question": "Can RTI score effectively separate adversarial chunks from benign context?",
        "metrics": "RTI Score Distribution, Density",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Critical",
        "section": "Defense Methodology",
        "selected_for_paper": True,
        "new_name": "figure5_ragshield_architecture.png",
        "paper_num": "Figure 5",
        "caption": "Distribution of Retrieval Trust Index (RTI) Scores for Clean vs. Poisoned Context Chunks Under RAGShield Defense."
    },
    {
        "id": "FIG-06",
        "filename": "asr_before_after.png",
        "location": "reports/phase6/figures/asr_before_after.png",
        "phase": "Phase 6",
        "purpose": "Compares Attack Success Rate before and after enabling RAGShield across models.",
        "question": "Does RAGShield effectively mitigate attack success across diverse LLM backbones?",
        "metrics": "ASR Before (%) vs ASR After (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Critical",
        "section": "Defense Evaluation",
        "selected_for_paper": True,
        "new_name": "figure6_defense_evaluation.png",
        "paper_num": "Figure 6",
        "caption": "Comparative Attack Success Rate (ASR) Before and After RAGShield Retrieval Trust Framework Deployment across Models."
    },
    {
        "id": "FIG-07",
        "filename": "security_vs_utility_pareto.png",
        "location": "reports/phase6_5/optimization/figures/security_vs_utility_pareto.png",
        "phase": "Phase 6.5",
        "purpose": "Plots the Pareto frontier of Security (ASR reduction) versus Utility (Clean QA containment).",
        "question": "What is the optimal operational threshold balancing security defense and QA utility?",
        "metrics": "ASR (%), Containment Utility (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "High",
        "section": "Adaptive Optimization & Tradeoffs",
        "selected_for_paper": True,
        "new_name": "figure7_security_utility_pareto.png",
        "paper_num": "Figure 7",
        "caption": "Pareto Optimization Curve Illustrating the Security–Utility Tradeoff Across Minimum RTI Threshold Configurations."
    },
    {
        "id": "FIG-08",
        "filename": "rcr_vs_attack_ratio.png",
        "location": "reports/phase4b_extension/figures/rcr_vs_attack_ratio.png",
        "phase": "Phase 4B Extension",
        "purpose": "Measures Retrieval Corruption Rate scaling with poison density.",
        "question": "How quickly does RCR saturate as poison ratio increases?",
        "metrics": "RCR (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-02",
        "priority": "Medium",
        "section": "Supplementary / Threat Model",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Retrieval Corruption Rate Scaling with Attack Ratio."
    },
    {
        "id": "FIG-09",
        "filename": "asr_vs_attack_ratio.png",
        "location": "reports/phase4b_extension/figures/asr_vs_attack_ratio.png",
        "phase": "Phase 4B Extension",
        "purpose": "Measures Attack Success Rate scaling with poison density.",
        "question": "Does higher poison ratio linearly increase LLM attack success?",
        "metrics": "ASR (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-02",
        "priority": "Medium",
        "section": "Supplementary / Threat Model",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Attack Success Rate Scaling with Attack Ratio."
    },
    {
        "id": "FIG-10",
        "filename": "targeted_vs_untargeted_asr.png",
        "location": "reports/phase4b_extension/figures/targeted_vs_untargeted_asr.png",
        "phase": "Phase 4B Extension",
        "purpose": "Compares targeted ASR against untargeted injection ASR.",
        "question": "Is targeted injection more successful than generic prompt hijacking?",
        "metrics": "Targeted ASR vs Untargeted ASR (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-03",
        "priority": "Medium",
        "section": "Supplementary / Threat Model",
        "selected_for_paper": False,
        "new_name": None,
        "caption": "Targeted vs Untargeted Attack Success Comparison."
    },
    {
        "id": "FIG-11",
        "filename": "targeted_vs_untargeted_rcr.png",
        "location": "reports/phase4b_extension/figures/targeted_vs_untargeted_rcr.png",
        "phase": "Phase 4B Extension",
        "purpose": "Compares targeted RCR against untargeted injection RCR.",
        "question": "Does targeted poisoning achieve higher retrieval penetration?",
        "metrics": "Targeted RCR vs Untargeted RCR (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-02",
        "priority": "Medium",
        "section": "Supplementary / Threat Model",
        "selected_for_paper": False,
        "new_name": None,
        "caption": "Targeted vs Untargeted Retrieval Corruption Comparison."
    },
    {
        "id": "FIG-12",
        "filename": "attack_category_comparison.png",
        "location": "reports/phase4c/figures/attack_category_comparison.png",
        "phase": "Phase 4C",
        "purpose": "Multi-axis comparison of 4 attack categories.",
        "question": "How do attack categories compare in terms of latency, RCR, and ASR?",
        "metrics": "RCR, ASR, Latency",
        "quality": "Yes",
        "redundancy": "Similar to FIG-03",
        "priority": "Medium",
        "section": "Supplementary / Results",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Multi-Metric Comparison Across Attack Categories."
    },
    {
        "id": "FIG-13",
        "filename": "rcr_by_attack_category.png",
        "location": "reports/phase4c/figures/rcr_by_attack_category.png",
        "phase": "Phase 4C",
        "purpose": "Retrieval corruption rate per attack category.",
        "question": "Which attack category penetrates FAISS retrieval most effectively?",
        "metrics": "RCR (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-03",
        "priority": "Medium",
        "section": "Supplementary / Results",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "RCR Breakdown by Attack Category."
    },
    {
        "id": "FIG-14",
        "filename": "attack_pipeline_sankey.png",
        "location": "reports/phase4f/figures/attack_pipeline_sankey.png",
        "phase": "Phase 4F",
        "purpose": "Sankey flow diagram of query progression from corpus to final output.",
        "question": "Where are attack payloads lost in the pipeline flow?",
        "metrics": "Flow counts (queries)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-01",
        "priority": "Medium",
        "section": "Supplementary / Discussion",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Sankey Flow Diagram of Attack Payload Progression."
    },
    {
        "id": "FIG-15",
        "filename": "failure_modes_by_model.png",
        "location": "reports/phase4f/figures/failure_modes_by_model.png",
        "phase": "Phase 4F",
        "purpose": "Failure mode distribution across Mistral, Qwen2.5, and Llama3.1.",
        "question": "Do different LLM backbones exhibit distinct prompt resistance behaviors?",
        "metrics": "Failure Mode % by Model",
        "quality": "Yes",
        "redundancy": "Similar to FIG-04",
        "priority": "Medium",
        "section": "Supplementary / Discussion",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Failure Mode Distribution Across LLM Backbones."
    },
    {
        "id": "FIG-16",
        "filename": "model_vs_attack_heatmap.png",
        "location": "reports/phase6/baseline/figures/model_vs_attack_heatmap.png",
        "phase": "Phase 6 Baseline",
        "purpose": "Heatmap of model performance across attack vectors.",
        "question": "Which model-attack pairs represent the highest vulnerability matrix?",
        "metrics": "ASR (%) Heatmap",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Medium",
        "section": "Supplementary / Model Sensitivity",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Model vs Attack Category Vulnerability Heatmap."
    },
    {
        "id": "FIG-17",
        "filename": "rcr_before_after.png",
        "location": "reports/phase6/figures/rcr_before_after.png",
        "phase": "Phase 6",
        "purpose": "Compares RCR before and after RAGShield.",
        "question": "Does RAGShield reduce retrieval corruption?",
        "metrics": "RCR Before vs After (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-06",
        "priority": "Medium",
        "section": "Supplementary / Defense Evaluation",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "RCR Before and After Defense Deployment."
    },
    {
        "id": "FIG-18",
        "filename": "threshold_vs_rates.png",
        "location": "reports/phase6_5/optimization/figures/threshold_vs_rates.png",
        "phase": "Phase 6.5",
        "purpose": "Plots threshold sensitivity vs RCR and False Positive Rate (FPR).",
        "question": "How does minimum RTI score impact false positive rate?",
        "metrics": "RCR (%), FPR (%)",
        "quality": "Yes",
        "redundancy": "Similar to FIG-07",
        "priority": "Medium",
        "section": "Supplementary / Optimization",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "RTI Threshold Sensitivity Curve."
    },
    {
        "id": "FIG-19",
        "filename": "trust_weight_heatmap.png",
        "location": "reports/phase6_5/optimization/figures/trust_weight_heatmap.png",
        "phase": "Phase 6.5",
        "purpose": "Heatmap of Optimization Scores across alpha/beta/gamma weight grid.",
        "question": "What weight balance maximizes the Retrieval Trust Index performance?",
        "metrics": "Optimization Score Heatmap",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Medium",
        "section": "Supplementary / Optimization",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Trust Weight Hyperparameter Grid Search Heatmap."
    },
    {
        "id": "FIG-20",
        "filename": "accuracy_by_corpus.png",
        "location": "reports/phase4d/figures/accuracy_by_corpus.png",
        "phase": "Phase 4D",
        "purpose": "Clean QA Accuracy across evaluation corpora.",
        "question": "Does poisoning corrupt clean query answers?",
        "metrics": "Accuracy (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Low",
        "section": "Supplementary / Utility Impact",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Clean QA Accuracy Across Corpora."
    },
    {
        "id": "FIG-21",
        "filename": "attack_vs_accuracy_tradeoff.png",
        "location": "reports/phase4d/figures/attack_vs_accuracy_tradeoff.png",
        "phase": "Phase 4D",
        "purpose": "Tradeoff curve between attack success and QA accuracy degradation.",
        "question": "Is QA accuracy inversely proportional to attack success?",
        "metrics": "Accuracy (%) vs ASR (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Low",
        "section": "Supplementary / Utility Impact",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Attack Success vs Accuracy Degradation Tradeoff."
    },
    {
        "id": "FIG-22",
        "filename": "containment_accuracy_by_corpus.png",
        "location": "reports/phase4d_reanalysis/figures/containment_accuracy_by_corpus.png",
        "phase": "Phase 4D Reanalysis",
        "purpose": "Containment-based accuracy reanalysis across corpora.",
        "question": "How does exact containment metric compare to EM/F1 for QA evaluation?",
        "metrics": "Containment Accuracy (%)",
        "quality": "Yes",
        "redundancy": "None",
        "priority": "Low",
        "section": "Supplementary / Reanalysis",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Containment-Based QA Accuracy Across Corpora."
    }
]

# 2. Table Inventory Data
tables_data = [
    {
        "id": "TBL-01",
        "filename": "Table_1_Attack_Configuration_Summary.md",
        "location": "reports/phase4b_extension/tables/Table_1_Attack_Configuration_Summary.md",
        "phase": "Phase 4B Extension",
        "purpose": "Summarizes the dataset sizes, chunk counts, attack types, and corpus configurations.",
        "metrics": "Corpus Name, Total Chunks, Poison Ratio, Attack Vector",
        "priority": "Critical",
        "section": "Experimental Setup",
        "selected_for_paper": True,
        "new_name": "table1_attack_summary.md",
        "paper_num": "Table 1",
        "caption": "Summary of Evaluated Corpora, Attack Vectors, and Dataset Configurations."
    },
    {
        "id": "TBL-02",
        "filename": "Table_All_Categories_Comparison.md",
        "location": "reports/phase4c/tables/Table_All_Categories_Comparison.md",
        "phase": "Phase 4C",
        "purpose": "Comparative security performance across Knowledge Poisoning, Instruction Injection, Goal Hijacking, and Information Extraction.",
        "metrics": "RCR (%), ASR (%), Latency Overhead (ms)",
        "priority": "Critical",
        "section": "Results & Vulnerability Analysis",
        "selected_for_paper": True,
        "new_name": "table2_category_comparison.md",
        "paper_num": "Table 2",
        "caption": "Comprehensive Security Performance Across Four Attack Categories."
    },
    {
        "id": "TBL-03",
        "filename": "Table_1_Overall_QA_Performance.md",
        "location": "reports/phase4d/tables/Table_1_Overall_QA_Performance.md",
        "phase": "Phase 4D",
        "purpose": "Evaluates baseline QA performance across Mistral, Qwen2.5:7b, and Llama3.1:8b backbones.",
        "metrics": "Exact Match (EM), F1-Score, Containment Accuracy (%)",
        "priority": "Critical",
        "section": "Model Sensitivity Analysis",
        "selected_for_paper": True,
        "new_name": "table3_multimodel_eval.md",
        "paper_num": "Table 3",
        "caption": "Baseline QA Accuracy and Containment Performance Across LLM Architectures."
    },
    {
        "id": "TBL-04",
        "filename": "Optimization_Summary.md",
        "location": "reports/phase6_5/optimization/analysis/Optimization_Summary.md",
        "phase": "Phase 6.5",
        "purpose": "Summarizes RAGShield defense performance, RCR mitigation, ASR drop, and containment utility.",
        "metrics": "RCR (%), ASR (%), Containment Utility (%), Latency (ms)",
        "priority": "Critical",
        "section": "Defense Evaluation",
        "selected_for_paper": True,
        "new_name": "table4_ragshield_performance.md",
        "paper_num": "Table 4",
        "caption": "RAGShield Defense System Performance and Containment Utility."
    },
    {
        "id": "TBL-05",
        "filename": "Weight_Search_Results.md",
        "location": "reports/phase6_5/optimization/analysis/Weight_Search_Results.md",
        "phase": "Phase 6.5",
        "purpose": "Details Stage 1 offline grid search results for RTI weight parameter optimization.",
        "metrics": "Alpha, Beta, Gamma, Threshold, RCR (%), FPR (%), Optimization Score",
        "priority": "High",
        "section": "Optimization & Hyperparameter Search",
        "selected_for_paper": True,
        "new_name": "table5_optimization_results.md",
        "paper_num": "Table 5",
        "caption": "Stage 1 Offline Grid Search Results for Retrieval Trust Index (RTI) Weight Optimization."
    },
    {
        "id": "TBL-06",
        "filename": "Table_3_System_Resource_Utilization.md",
        "location": "reports/phase4b_extension/tables/Table_3_System_Resource_Utilization.md",
        "phase": "Phase 4B Extension",
        "purpose": "Measures memory footprint (VRAM/RAM) and microsecond latency per component.",
        "metrics": "RAM (MB), VRAM (MB), Retrieval Latency (ms), Scorer Latency (ms)",
        "priority": "High",
        "section": "System Efficiency & Overhead",
        "selected_for_paper": True,
        "new_name": "table6_system_overhead.md",
        "paper_num": "Table 6",
        "caption": "System Resource Utilization, Memory Footprint, and Microsecond Latency Overhead."
    },
    {
        "id": "TBL-07",
        "filename": "Table_KP_vs_Instruction_Injection.md",
        "location": "reports/phase4c/tables/Table_KP_vs_Instruction_Injection.md",
        "phase": "Phase 4C",
        "purpose": "Direct head-to-head metrics for Knowledge Poisoning vs Instruction Injection.",
        "metrics": "Delta RCR (%), Delta ASR (%)",
        "priority": "Medium",
        "section": "Supplementary",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Knowledge Poisoning vs Instruction Injection Metrics."
    },
    {
        "id": "TBL-08",
        "filename": "Table_KP_vs_Goal_Hijacking.md",
        "location": "reports/phase4c/tables/Table_KP_vs_Goal_Hijacking.md",
        "phase": "Phase 4C",
        "purpose": "Head-to-head metrics for Knowledge Poisoning vs Goal Hijacking.",
        "metrics": "Delta RCR (%), Delta ASR (%)",
        "priority": "Medium",
        "section": "Supplementary",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Knowledge Poisoning vs Goal Hijacking Metrics."
    },
    {
        "id": "TBL-09",
        "filename": "Table_KP_vs_Information_Extraction.md",
        "location": "reports/phase4c/tables/Table_KP_vs_Information_Extraction.md",
        "phase": "Phase 4C",
        "purpose": "Head-to-head metrics for Knowledge Poisoning vs Information Extraction.",
        "metrics": "Delta RCR (%), Delta ASR (%)",
        "priority": "Medium",
        "section": "Supplementary",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Knowledge Poisoning vs Information Extraction Metrics."
    },
    {
        "id": "TBL-10",
        "filename": "transition_table.md",
        "location": "reports/phase4f/tables/transition_table.md",
        "phase": "Phase 4F",
        "purpose": "State transition counts from Retrieval to Generation stages.",
        "metrics": "Transition probabilities, Query counts",
        "priority": "Medium",
        "section": "Supplementary",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "State Transition Counts Across Pipeline Stages."
    },
    {
        "id": "TBL-11",
        "filename": "Table_2_Relative_Accuracy_Degradation.md",
        "location": "reports/phase4d/tables/Table_2_Relative_Accuracy_Degradation.md",
        "phase": "Phase 4D",
        "purpose": "Measures relative degradation in QA accuracy due to adversarial presence.",
        "metrics": "Relative Accuracy Drop (%)",
        "priority": "Medium",
        "section": "Supplementary",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Relative Accuracy Degradation Across Corpora."
    },
    {
        "id": "TBL-12",
        "filename": "Table_3_Dataset_Breakdown.md",
        "location": "reports/phase4d/tables/Table_3_Dataset_Breakdown.md",
        "phase": "Phase 4D",
        "purpose": "Breakdown of benchmark dataset questions and ground truth lengths.",
        "metrics": "Question Count, Avg Word Length",
        "priority": "Low",
        "section": "Supplementary",
        "selected_for_paper": False,
        "new_name": None,
        "paper_num": None,
        "caption": "Evaluation Dataset Word Count and Question Distribution."
    }
]

# Generate Step 2 & 3: Figure_Inventory.md
fig_inv_content = """# Master Figure Inventory & Publication Selection

This document contains a comprehensive audit of all visual artifacts generated across Phases 4A through 6.5 of the RAPTOR project, including candidate rankings and final selection rationale for the 6-page IEEE paper.

---

## 1. Complete Repository Figure Audit

"""

for f in figures_data:
    fig_inv_content += f"""------------------------------------------------
### {f['id']}: {f['filename']}
- **Current Location**: `{f['location']}`
- **Phase**: {f['phase']}
- **Purpose**: {f['purpose']}
- **Scientific Question Answered**: {f['question']}
- **Metrics Shown**: {f['metrics']}
- **Publication Quality**: {f['quality']}
- **Redundancy**: {f['redundancy']}
- **Recommended Priority**: {f['priority']}
- **Estimated Paper Section**: {f['section']}
- **Selection Status**: {'SELECTED for Paper (' + f['paper_num'] + ': ' + f['new_name'] + ')' if f['selected_for_paper'] else 'Excluded (Moved to Supplementary)'}

"""

fig_inv_content += """---

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
"""

with open(os.path.join(PAPER_ASSETS_DIR, "Figure_Inventory.md"), "w") as f:
    f.write(fig_inv_content)

print("Figure_Inventory.md written successfully.")

# Generate Step 7: Table_Inventory.md
tbl_inv_content = """# Master Table Inventory & Publication Selection

This document contains a comprehensive audit of all tables generated across Phases 4A through 6.5 of the RAPTOR project, including selection rationale for the 6-page IEEE paper.

---

## 1. Complete Repository Table Audit

"""

for t in tables_data:
    tbl_inv_content += f"""------------------------------------------------
### {t['id']}: {t['filename']}
- **Current Location**: `{t['location']}`
- **Phase**: {t['phase']}
- **Purpose**: {t['purpose']}
- **Metrics Shown**: {t['metrics']}
- **Recommended Priority**: {t['priority']}
- **Estimated Paper Section**: {t['section']}
- **Selection Status**: {'SELECTED for Paper (' + t['paper_num'] + ': ' + t['new_name'] + ')' if t['selected_for_paper'] else 'Excluded (Moved to Supplementary)'}

"""

tbl_inv_content += """---

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
"""

with open(os.path.join(PAPER_ASSETS_DIR, "Table_Inventory.md"), "w") as f:
    f.write(tbl_inv_content)

print("Table_Inventory.md written successfully.")

# Step 5 & 6: Copy files to paper/figures and paper/tables, write FIGURE_MAPPING.md & TABLE_MAPPING.md

fig_map_content = """# IEEE Paper Figure Mapping

This document maps original repository figure files to their standardized publication names and captions in `paper/figures/`.

| Paper Figure Number | Standardized Filename | Original Filename | Original Location | Paper Section | Caption Title |
|---|---|---|---|---|---|
"""

for f in figures_data:
    if f["selected_for_paper"]:
        src_path = f["location"]
        dst_path = os.path.join(PAPER_FIGS_DIR, f["new_name"])
        shutil.copyfile(src_path, dst_path)
        fig_map_content += f"| {f['paper_num']} | `{f['new_name']}` | `{f['filename']}` | `{f['location']}` | {f['section']} | {f['caption']} |\n"

with open(os.path.join(PAPER_FIGS_DIR, "FIGURE_MAPPING.md"), "w") as f:
    f.write(fig_map_content)

print("FIGURE_MAPPING.md written and figures copied.")

tbl_map_content = """# IEEE Paper Table Mapping

This document maps original repository table files to their standardized publication names and captions in `paper/tables/`.

| Paper Table Number | Standardized Filename | Original Filename | Original Location | Paper Section | Caption Title |
|---|---|---|---|---|---|
"""

for t in tables_data:
    if t["selected_for_paper"]:
        src_path = t["location"]
        dst_path = os.path.join(PAPER_TBLS_DIR, t["new_name"])
        shutil.copyfile(src_path, dst_path)
        tbl_map_content += f"| {t['paper_num']} | `{t['new_name']}` | `{t['filename']}` | `{t['location']}` | {t['section']} | {t['caption']} |\n"

with open(os.path.join(PAPER_TBLS_DIR, "TABLE_MAPPING.md"), "w") as f:
    f.write(tbl_map_content)

print("TABLE_MAPPING.md written and tables copied.")

# Step 8: Generate paper/PAPER_ASSETS.md
paper_assets_master = """# IEEE Manuscript Master Asset Reference

This document serves as the single source of truth for all publication figures, tables, and supplementary assets during manuscript authoring.

====================================================

## FINAL PUBLICATION FIGURES

### Figure 1: Threat Model & Pipeline Flow
- **Filename**: `paper/figures/figure1_attack_pipeline.png`
- **Original Source**: `reports/phase4c/figures/attack_pipeline_breakdown.png`
- **Section**: Section II (Threat Model & Background)
- **Caption**: *End-to-End Poisoning Flow and Information Degradation across the RAG Retrieval-Generation Lifecycle.*
- **Scientific Role**: Establishes how adversarial chunks penetrate retrieval and progress to generation.

### Figure 2: Targeted vs Random Poisoning Efficiency
- **Filename**: `paper/figures/figure2_retrieval_poisoning.png`
- **Original Source**: `reports/phase4b_extension/figures/targeted_vs_random_poisoning.png`
- **Section**: Section IV (Empirical Threat Analysis)
- **Caption**: *Retrieval Corruption Rate (RCR) and Attack Success Rate (ASR) Comparison Between Targeted Retrieval-Aware Poisoning and Random Poisoning.*
- **Scientific Role**: Demonstrates that semantic-aware targeted poisoning achieves ~99% RCR versus failure of random noise.

### Figure 3: Vulnerability Profile Across Attack Vectors
- **Filename**: `paper/figures/figure3_attack_categories.png`
- **Original Source**: `reports/phase4c/figures/asr_by_attack_category.png`
- **Section**: Section IV (Empirical Threat Analysis)
- **Caption**: *Vulnerability Profile and Attack Success Rate Across Diverse Injection Tactics (Knowledge Poisoning, Instruction Injection, Goal Hijacking, Information Extraction).*
- **Scientific Role**: Maps security posture across four distinct prompt injection vectors.

### Figure 4: Generation Bottleneck & Failure Modes
- **Filename**: `paper/figures/figure4_failure_modes.png`
- **Original Source**: `reports/phase4f/figures/failure_modes_by_attack.png`
- **Section**: Section V (Failure Mode & Bottleneck Analysis)
- **Caption**: *Categorical Breakdown of Pipeline Bottlenecks and Failure Modes Indicating Prompt Resistance during Generation.*
- **Scientific Role**: Explains why high RCR (~99%) does not yield high ASR (~5%) due to LLM prior dominance and prompt resistance.

### Figure 5: RAGShield Retrieval Trust Index Density
- **Filename**: `paper/figures/figure5_ragshield_architecture.png`
- **Original Source**: `reports/phase6/figures/trust_index_distribution.png`
- **Section**: Section VI (RAGShield Defense System)
- **Caption**: *Distribution of Retrieval Trust Index (RTI) Scores for Clean vs. Poisoned Context Chunks Under RAGShield Defense.*
- **Scientific Role**: Visualizes score separation between benign context and adversarial payloads under RTI scoring.

### Figure 6: Defense Effectiveness (Before vs After)
- **Filename**: `paper/figures/figure6_defense_evaluation.png`
- **Original Source**: `reports/phase6/figures/asr_before_after.png`
- **Section**: Section VII (Defense Evaluation & Results)
- **Caption**: *Comparative Attack Success Rate (ASR) Before and After RAGShield Retrieval Trust Framework Deployment across Models.*
- **Scientific Role**: Core empirical validation of defense impact across Mistral, Qwen2.5, and Llama3.1.

### Figure 7: Security vs Utility Pareto Frontier
- **Filename**: `paper/figures/figure7_security_utility_pareto.png`
- **Original Source**: `reports/phase6_5/optimization/figures/security_vs_utility_pareto.png`
- **Section**: Section VII (Adaptive Optimization & Tradeoffs)
- **Caption**: *Pareto Optimization Curve Illustrating the Security–Utility Tradeoff Across Minimum RTI Threshold Configurations.*
- **Scientific Role**: Illustrates operational trade-off between ASR reduction and clean QA containment utility.

====================================================

## FINAL PUBLICATION TABLES

### Table 1: Attack Corpus & Dataset Configuration Summary
- **Filename**: `paper/tables/table1_attack_summary.md`
- **Original Source**: `reports/phase4b_extension/tables/Table_1_Attack_Configuration_Summary.md`
- **Section**: Section III (Experimental Methodology)
- **Caption**: *Summary of Evaluated Corpora, Attack Vectors, and Dataset Configurations.*

### Table 2: Vulnerability Benchmark Across Attack Categories
- **Filename**: `paper/tables/table2_category_comparison.md`
- **Original Source**: `reports/phase4c/tables/Table_All_Categories_Comparison.md`
- **Section**: Section IV (Empirical Threat Analysis)
- **Caption**: *Comprehensive Security Performance Across Four Attack Categories.*

### Table 3: Multi-Model QA Baseline Evaluation
- **Filename**: `paper/tables/table3_multimodel_eval.md`
- **Original Source**: `reports/phase4d/tables/Table_1_Overall_QA_Performance.md`
- **Section**: Section IV (Model Sensitivity Analysis)
- **Caption**: *Baseline QA Accuracy and Containment Performance Across LLM Architectures.*

### Table 4: RAGShield Defense System Performance Summary
- **Filename**: `paper/tables/table4_ragshield_performance.md`
- **Original Source**: `reports/phase6_5/optimization/analysis/Optimization_Summary.md`
- **Section**: Section VII (Defense Evaluation)
- **Caption**: *RAGShield Defense System Performance and Containment Utility.*

### Table 5: Stage 1 RTI Weight Grid Search Optimization
- **Filename**: `paper/tables/table5_optimization_results.md`
- **Original Source**: `reports/phase6_5/optimization/analysis/Weight_Search_Results.md`
- **Section**: Section VII (Adaptive Optimization & Tradeoffs)
- **Caption**: *Stage 1 Offline Grid Search Results for Retrieval Trust Index (RTI) Weight Optimization.*

### Table 6: System Resource Footprint and Overhead
- **Filename**: `paper/tables/table6_system_overhead.md`
- **Original Source**: `reports/phase4b_extension/tables/Table_3_System_Resource_Utilization.md`
- **Section**: Section VIII (System Efficiency & Latency)
- **Caption**: *System Resource Utilization, Memory Footprint, and Microsecond Latency Overhead.*

====================================================

## SUPPLEMENTARY FIGURES (EXCLUDED & RATIONALE)

"""

for f in figures_data:
    if not f["selected_for_paper"]:
        paper_assets_master += f"""### {f['id']}: {f['filename']}
- **Location**: `{f['location']}`
- **Reason for Exclusion**: {f['redundancy']}. Retained as supplementary data for extended technical appendix.

"""

paper_assets_master += """====================================================

## SUPPLEMENTARY TABLES (EXCLUDED & RATIONALE)

"""

for t in tables_data:
    if not t["selected_for_paper"]:
        paper_assets_master += f"""### {t['id']}: {t['filename']}
- **Location**: `{t['location']}`
- **Reason for Exclusion**: Detailed pairwise breakdown ({t['purpose']}). Content summarized in main Table 2. Retained for appendix reference.

"""

with open(os.path.join(PAPER_DIR, "PAPER_ASSETS.md"), "w") as f:
    f.write(paper_assets_master)

print("PAPER_ASSETS.md written successfully.")
