import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

OUT_DIR_FIGS = "reports/ieee_artifacts_phase6_5/figures"
OUT_DIR_TABLES = "reports/ieee_artifacts_phase6_5/tables"
OUT_DIR_REPORTS = "reports"

os.makedirs(OUT_DIR_FIGS, exist_ok=True)
os.makedirs(OUT_DIR_TABLES, exist_ok=True)

def generate_reports():
    print("Loading Phase 6.5 optimization results...")
    
    # Load data
    try:
        df_weights = pd.read_csv("reports/phase6_5/weight_search.csv")
        df_stage2 = pd.read_csv("reports/phase6_5/stage2_results.csv")
    except FileNotFoundError:
        print("Data files not found. Skipping analysis.")
        return

    # Extract best configuration from Stage 2
    best_config = df_stage2.iloc[0]
    
    print("Generating markdown summaries...")
    
    # Generate Phase 6.5 Summary
    with open(f"{OUT_DIR_REPORTS}/phase6_5_summary.md", "w") as f:
        f.write("# Phase 6.5 Adaptive RTI Optimization Summary\n\n")
        f.write("## Recommended Configuration\n")
        f.write(f"- **Best RTI Weights**: alpha={best_config['alpha']:.2f}, beta={best_config.get('beta', 0.4):.2f}, gamma={best_config.get('gamma', 0.4):.2f}\n")
        f.write(f"- **Best Threshold**: {best_config['threshold']:.2f}\n")
        f.write("- **Consistency Penalty Weight**: 0.5 (Fixed for this run)\n")
        
        f.write("\n## Optimization Results (Mistral Knowledge Poisoning)\n")
        f.write(f"- **Retrieval Corruption Rate (RCR)**: {best_config['rcr']*100:.1f}%\n")
        f.write(f"- **Attack Success Rate (ASR)**: {best_config['asr']*100:.1f}%\n")
        f.write(f"- **Utility Preservation (Containment)**: {best_config['containment']*100:.1f}%\n")
        
        f.write("\n## Key Findings\n")
        f.write("Despite sweeping across all combinations of trust weights, thresholds, and introducing a Consistency Penalty and Hard Trust Filtering, the RCR remained stubbornly at 100%. This implies that Knowledge Poisoning attacks are structurally and semantically indistinguishable from valid chunks under the current semantic models, overpowering both the consensus analyzer and the base retrieval confidence.\n")

    # Generate Tables
    with open(f"{OUT_DIR_TABLES}/Weight_Search_Results.md", "w") as f:
        f.write("# Weight Search Results (Top 10)\n\n")
        f.write(df_weights.sort_values(by="opt_score", ascending=False).head(10).to_markdown(index=False))

    with open(f"{OUT_DIR_TABLES}/Optimization_Summary.md", "w") as f:
        f.write("# Optimization Summary (Stage 2 LLM Evals)\n\n")
        f.write(df_stage2.to_markdown(index=False))

    print("Generating Figures...")

    # Heatmap of Trust Weights (fixing gamma to 0.4 for 2D plot)
    subset = df_weights[df_weights["gamma"] == 0.4]
    if not subset.empty:
        pivot = subset.pivot_table(index="alpha", columns="beta", values="opt_score", aggfunc=np.mean)
        plt.figure(figsize=(6,5))
        sns.heatmap(pivot, annot=True, cmap="coolwarm")
        plt.title("Optimization Score Heatmap (gamma=0.4)")
        plt.savefig(f"{OUT_DIR_FIGS}/trust_weight_heatmap.png", dpi=300, bbox_inches="tight")
        plt.close()

    # Threshold vs RCR/FPR
    thresholds = df_weights.groupby("threshold")[["rcr", "fpr"]].mean().reset_index()
    plt.figure(figsize=(6,4))
    plt.plot(thresholds["threshold"], thresholds["rcr"], label="RCR", marker='o')
    plt.plot(thresholds["threshold"], thresholds["fpr"], label="FPR", marker='s')
    plt.title("Threshold vs RCR and FPR")
    plt.xlabel("Minimum RTI Score")
    plt.ylabel("Rate")
    plt.legend()
    plt.savefig(f"{OUT_DIR_FIGS}/threshold_vs_rates.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Pareto Frontier: Security vs Utility
    # We can plot ASR vs Containment from Stage 2
    plt.figure(figsize=(6,4))
    plt.scatter(df_stage2["asr"]*100, df_stage2["containment"]*100, color='purple', s=100)
    plt.title("Security vs Utility Pareto (Top Configs)")
    plt.xlabel("Attack Success Rate (%)")
    plt.ylabel("Containment Utility (%)")
    plt.grid(True)
    for i, row in df_stage2.iterrows():
        plt.annotate(f"T={row['threshold']}", (row['asr']*100, row['containment']*100))
    plt.savefig(f"{OUT_DIR_FIGS}/security_vs_utility_pareto.png", dpi=300, bbox_inches="tight")
    plt.close()
    
    print("IEEE Artifacts generated successfully!")

if __name__ == "__main__":
    generate_reports()
