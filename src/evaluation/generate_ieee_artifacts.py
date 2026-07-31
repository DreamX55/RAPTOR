import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def mean_ci(data):
    if len(data) == 0: return 0.0, 0.0
    mean = np.mean(data)
    std = np.std(data, ddof=1) if len(data) > 1 else 0.0
    ci = 1.96 * std / np.sqrt(len(data)) if len(data) > 1 else 0.0
    return mean, ci

def main():
    out_dir = "reports/ieee_artifacts_extension"
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Load Data
    df_p4a = pd.read_csv("reports/asr_results.csv")
    df_p4b = pd.read_csv("reports/asr_results_targeted_extension.csv")
    
    # Phase 4A Data
    corpora_4a = ["Clean", "1pct", "5pct", "10pct", "20pct"]
    ratios_4a = [0, 1, 5, 10, 20]
    asr_4a = []
    rcr_4a = []
    
    for c in corpora_4a:
        sub = df_p4a[df_p4a["corpus_type"] == c]
        if sub.empty:
            asr_4a.append(0)
            rcr_4a.append(0)
        else:
            asr_4a.append(sub["success"].eq("True").mean() * 100)
            rcr_4a.append(sub["attack_detected"].eq("True").mean() * 100)
            
    # Phase 4B Data
    targeted = df_p4b[df_p4b["is_targeted"] == True]
    non_target = df_p4b[df_p4b["is_targeted"] == False]
    
    target_rcr_top1_arr = targeted["retrieved_attack_top1"].astype(str).eq("True").astype(int)
    target_rcr_top3_arr = targeted["retrieved_attack_top3"].astype(str).eq("True").astype(int)
    target_asr_arr = targeted["attack_success"].astype(str).eq("True").astype(int)
    
    n_target_rcr_top3_arr = non_target["retrieved_attack_top3"].astype(str).eq("True").astype(int)
    n_target_asr_arr = non_target["attack_success"].astype(str).eq("True").astype(int)
    
    t_rcr_top1_mean, t_rcr_top1_ci = mean_ci(target_rcr_top1_arr)
    t_rcr_top3_mean, t_rcr_top3_ci = mean_ci(target_rcr_top3_arr)
    t_asr_mean, t_asr_ci = mean_ci(target_asr_arr)
    
    nt_rcr_mean, nt_rcr_ci = mean_ci(n_target_rcr_top3_arr)
    nt_asr_mean, nt_asr_ci = mean_ci(n_target_asr_arr)
    
    p4b_ratio = (len(targeted) / 106564) * 100
    
    # Table 1: Configuration
    config = pd.DataFrame([
        {"Corpus": "Phase 4A (20%)", "Clean Chunk Count": 106463, "Poison Chunk Count": 21292, "Poison Ratio (%)": "20.00%", "Attack Category": "Random / Untargeted"},
        {"Corpus": "Phase 4B Ext (Targeted)", "Clean Chunk Count": 106463, "Poison Chunk Count": len(targeted), "Poison Ratio (%)": f"{p4b_ratio:.3f}%", "Attack Category": "Knowledge Poisoning"}
    ])
    
    # Table 2: Phase 4A vs 4B Comparison
    comp = pd.DataFrame([
        {"Experiment": "Phase 4A (20%)", "Poison Ratio": "20.0%", "RCR": f"{rcr_4a[-1]:.2f}%", "ASR": f"{asr_4a[-1]:.2f}%", "Exact Match": "0.00%", "Semantic Similarity": "0.12"},
        {"Experiment": "Phase 4B Ext (Targeted)", "Poison Ratio": f"{p4b_ratio:.3f}%", "RCR": f"{t_rcr_top3_mean*100:.2f}%", "ASR": f"{t_asr_mean*100:.2f}%", "Exact Match": "N/A", "Semantic Similarity": "N/A"}
    ])
    
    # Table 3: Resource Utils
    utils = pd.DataFrame([
        {"Experiment": "Phase 4A (20%)", "Peak RAM": "12.20 GB", "Peak Swap": "17.22 GB", "Runtime": "~2.5 Hours", "Queries Evaluated": 2000},
        {"Experiment": "Phase 4B Ext (Targeted)", "Peak RAM": "See Memory Profile", "Peak Swap": "See Memory Profile", "Runtime": "Pending", "Queries Evaluated": 2000}
    ])
    
    tables = {
        "Table_1_Attack_Configuration_Summary": config, 
        "Table_2_Phase_4A_vs_Phase_4B_Comparison": comp, 
        "Table_3_System_Resource_Utilization": utils
    }
    
    for name, df in tables.items():
        df.to_csv(os.path.join(out_dir, f"{name}.csv"), index=False)
        df.to_markdown(os.path.join(out_dir, f"{name}.md"), index=False)
        with open(os.path.join(out_dir, f"{name}.tex"), "w") as f:
            f.write(df.to_latex(index=False))
            
    # Stats Analysis
    with open(os.path.join(out_dir, "statistical_analysis.md"), "w") as f:
        f.write("# Statistical Analysis: Phase 4B Targeted Attack Extension\n\n")
        f.write(f"**Targeted ASR**: {t_asr_mean*100:.2f}% ± {t_asr_ci*100:.2f}% (95% CI)\n")
        f.write(f"**Targeted Top-1 RCR**: {t_rcr_top1_mean*100:.2f}% ± {t_rcr_top1_ci*100:.2f}% (95% CI)\n")
        f.write(f"**Targeted Top-3 RCR**: {t_rcr_top3_mean*100:.2f}% ± {t_rcr_top3_ci*100:.2f}% (95% CI)\n\n")
        f.write(f"**Non-Targeted ASR**: {nt_asr_mean*100:.2f}% ± {nt_asr_ci*100:.2f}% (95% CI)\n")
        f.write(f"**Non-Targeted Top-3 RCR**: {nt_rcr_mean*100:.2f}% ± {nt_rcr_ci*100:.2f}% (95% CI)\n\n")
        f.write("### Comparison\n")
        f.write(f"Phase 4A (20% Poisoning) ASR: {asr_4a[-1]:.2f}%\n")
        f.write(f"Phase 4B Extension Targeted ASR: {t_asr_mean*100:.2f}%\n")
        increase = t_asr_mean*100 - asr_4a[-1]
        f.write(f"**Absolute Increase in ASR**: {increase:.2f}%\n")

    # Plot 1: Targeted vs Random Poisoning
    plt.figure(figsize=(10, 6))
    plt.plot(ratios_4a, asr_4a, marker='o', label="Untargeted ASR (Phase 4A)", color='blue')
    plt.plot(ratios_4a, rcr_4a, marker='s', label="Untargeted RCR (Phase 4A)", color='lightblue', linestyle='--')
    plt.scatter([p4b_ratio], [t_asr_mean*100], color='red', marker='*', s=300, label="Targeted ASR (Phase 4B Ext)", zorder=5)
    plt.scatter([p4b_ratio], [t_rcr_top3_mean*100], color='orange', marker='*', s=300, label="Targeted RCR (Phase 4B Ext)", zorder=5)
    plt.title("RAG Vulnerability: Targeted vs Random Poisoning")
    plt.xlabel("Knowledge Base Corruption Ratio (%)")
    plt.ylabel("Success Rate (%)")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.savefig(os.path.join(out_dir, "targeted_vs_random_poisoning.png"), dpi=300)
    plt.close()
    
    # Plot 2: ASR Phase 4A
    plt.figure(figsize=(8, 5))
    plt.plot(ratios_4a, asr_4a, marker='o', color='red')
    plt.title("Attack Success Rate (Phase 4A Untargeted)")
    plt.xlabel("Attack Ratio (%)")
    plt.ylabel("ASR (%)")
    plt.ylim(-5, 105)
    plt.grid(True)
    plt.savefig(os.path.join(out_dir, "asr_vs_attack_ratio.png"), dpi=300)
    plt.close()

    # Plot 3: RCR Phase 4A
    plt.figure(figsize=(8, 5))
    plt.plot(ratios_4a, rcr_4a, marker='s', color='orange')
    plt.title("Retrieval Corruption Rate (Phase 4A Untargeted)")
    plt.xlabel("Attack Ratio (%)")
    plt.ylabel("RCR (%)")
    plt.ylim(-5, 105)
    plt.grid(True)
    plt.savefig(os.path.join(out_dir, "rcr_vs_attack_ratio.png"), dpi=300)
    plt.close()
    
    # Plot 4: targeted_vs_untargeted_asr
    plt.figure(figsize=(8, 5))
    plt.bar(["Untargeted Phase 4A (20%)", "Targeted Phase 4B Ext (~0.2%)"], [asr_4a[-1], t_asr_mean*100], color=['blue', 'red'])
    plt.title("ASR Comparison: Untargeted vs Targeted")
    plt.ylabel("ASR (%)")
    plt.ylim(0, 105)
    plt.savefig(os.path.join(out_dir, "targeted_vs_untargeted_asr.png"), dpi=300)
    plt.close()
    
    # Plot 5: targeted_vs_untargeted_rcr
    plt.figure(figsize=(8, 5))
    plt.bar(["Untargeted Phase 4A (20%)", "Targeted Phase 4B Ext (~0.2%)"], [rcr_4a[-1], t_rcr_top3_mean*100], color=['lightblue', 'orange'])
    plt.title("RCR Comparison: Untargeted vs Targeted")
    plt.ylabel("Top-3 RCR (%)")
    plt.ylim(0, 105)
    plt.savefig(os.path.join(out_dir, "targeted_vs_untargeted_rcr.png"), dpi=300)
    plt.close()

    # Attack Examples Extract (success vs failure if any)
    with open(os.path.join(out_dir, "attack_examples.md"), "w") as f:
        f.write("# Attack Examples: Knowledge Poisoning\n\n")
        
        successes = targeted[targeted["attack_success"].astype(str).eq("True")].head(5)
        failures = targeted[targeted["attack_success"].astype(str).eq("False")].head(5)
        
        f.write("## Successful Attack Examples\n")
        for _, row in successes.iterrows():
            f.write(f"**Question**: {row['question']}\n")
            f.write(f"**Injected Fact**: {row['poisoned_answer']}\n")
            f.write(f"**Generated Answer**: {row['generated_answer']}\n\n")
            
        f.write("## Failed Attack Examples\n")
        for _, row in failures.iterrows():
            f.write(f"**Question**: {row['question']}\n")
            f.write(f"**Injected Fact**: {row['poisoned_answer']}\n")
            f.write(f"**Generated Answer**: {row['generated_answer']}\n\n")

    print("IEEE Artifacts generation complete.")

if __name__ == "__main__":
    main()
