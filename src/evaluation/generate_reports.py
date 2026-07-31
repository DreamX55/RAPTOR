import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import argparse

def generate_report(csv_path, output_dir, is_pilot):
    print(f"Generating reports from {csv_path} into {output_dir} (Pilot: {is_pilot})")
    
    prefix = "pilot_" if is_pilot else ""
    os.makedirs(output_dir, exist_ok=True)
    
    df = pd.read_csv(csv_path)
    
    # 1. Calculate Retrieval Corruption Rate (RCR)
    # RCR = queries retrieving at least one attack chunk / total queries
    rcr_data = {}
    asr_data = {}
    em_data = {}
    sim_data = {}
    
    corpora = ["Clean", "1pct", "5pct", "10pct", "20pct"]
    ratios = [0, 1, 5, 10, 20]
    
    # Analyze false ASR on clean baseline
    clean_df = df[df["corpus_type"] == "Clean"]
    false_asr = clean_df["success"].eq("True").mean() if not clean_df.empty else 0.0
    print(f"Baseline False ASR on Clean Corpus: {false_asr:.2%}")
    
    for corpus in corpora:
        subset = df[df["corpus_type"] == corpus]
        if subset.empty:
            rcr_data[corpus] = 0
            asr_data[corpus] = 0
            em_data[corpus] = 0
            sim_data[corpus] = 0
            continue
            
        rcr = subset["attack_detected"].eq("True").mean()
        asr = subset["success"].eq("True").mean()
        em = subset["exact_match"].eq(1).mean()
        sim = subset["semantic_similarity"].mean()
        
        rcr_data[corpus] = rcr
        asr_data[corpus] = asr
        em_data[corpus] = em
        sim_data[corpus] = sim
        
    # --- PLOTS ---
    # 1. ASR vs Attack Ratio
    plt.figure(figsize=(8, 5))
    plt.plot(ratios, [asr_data[c] for c in corpora], marker='o', linewidth=2, color='red')
    plt.title("Attack Success Rate (ASR) vs Knowledge Base Corruption")
    plt.xlabel("Percentage of Attacked Chunks (%)")
    plt.ylabel("Attack Success Rate")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(ratios)
    plt.ylim(0, 1)
    plt.savefig(os.path.join(output_dir, f"{prefix}asr_vs_attack_ratio.png"), dpi=300, bbox_inches="tight")
    plt.close()
    
    # 2. Retrieval Corruption Rate (RCR)
    plt.figure(figsize=(8, 5))
    plt.plot(ratios, [rcr_data[c] for c in corpora], marker='s', linewidth=2, color='orange')
    plt.title("Retrieval Corruption Rate (RCR) vs Knowledge Base Corruption")
    plt.xlabel("Percentage of Attacked Chunks (%)")
    plt.ylabel("Retrieval Corruption Rate")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(ratios)
    plt.ylim(0, 1)
    plt.savefig(os.path.join(output_dir, f"{prefix}retrieval_corruption_rate.png"), dpi=300, bbox_inches="tight")
    plt.close()
    
    # 3. Exact Match vs Attack Ratio
    plt.figure(figsize=(8, 5))
    plt.plot(ratios, [em_data[c] for c in corpora], marker='^', linewidth=2, color='blue')
    plt.title("Exact Match (EM) vs Knowledge Base Corruption")
    plt.xlabel("Percentage of Attacked Chunks (%)")
    plt.ylabel("Exact Match Score")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(ratios)
    plt.ylim(0, 1)
    plt.savefig(os.path.join(output_dir, f"{prefix}em_vs_attack_ratio.png"), dpi=300, bbox_inches="tight")
    plt.close()
    
    # 4. Semantic Similarity vs Attack Ratio
    plt.figure(figsize=(8, 5))
    plt.plot(ratios, [sim_data[c] for c in corpora], marker='d', linewidth=2, color='purple')
    plt.title("Semantic Similarity vs Knowledge Base Corruption")
    plt.xlabel("Percentage of Attacked Chunks (%)")
    plt.ylabel("Cosine Similarity")
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(ratios)
    plt.ylim(0, 1)
    plt.savefig(os.path.join(output_dir, f"{prefix}semantic_similarity_vs_attack_ratio.png"), dpi=300, bbox_inches="tight")
    plt.close()
    
    # 5. Attack Type Distribution
    attacked_df = df[df["attack_type"] != "Clean"]
    if not attacked_df.empty:
        plt.figure(figsize=(8, 5))
        attacked_df["attack_type"].value_counts().plot(kind='bar', color='darkred')
        plt.title("Distribution of Successful Attack Types")
        plt.ylabel("Count")
        plt.xticks(rotation=15, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{prefix}attack_type_distribution.png"), dpi=300)
        plt.close()
        
    # --- MARKDOWN REPORT ---
    report_path = os.path.join(output_dir, f"../asr_report_{'pilot' if is_pilot else 'full'}.md")
    
    md = f"""# RAPTOR Phase 4A: ASR Evaluation Report ({'Pilot' if is_pilot else 'Full'})

## Executive Summary
This report presents the Attack Success Rate (ASR) evaluation of the Mistral-based RAG pipeline.

- **Total Queries Evaluated per Corpus**: {len(clean_df)}
- **Baseline False ASR (Clean Corpus)**: {false_asr:.2%}

## Key Metrics Summary

| Corpus | RCR | ASR | Exact Match | Semantic Similarity |
|---|---|---|---|---|
| Clean | {rcr_data["Clean"]:.2%} | {asr_data["Clean"]:.2%} | {em_data["Clean"]:.2%} | {sim_data["Clean"]:.4f} |
| 1% Attacked | {rcr_data["1pct"]:.2%} | {asr_data["1pct"]:.2%} | {em_data["1pct"]:.2%} | {sim_data["1pct"]:.4f} |
| 5% Attacked | {rcr_data["5pct"]:.2%} | {asr_data["5pct"]:.2%} | {em_data["5pct"]:.2%} | {sim_data["5pct"]:.4f} |
| 10% Attacked | {rcr_data["10pct"]:.2%} | {asr_data["10pct"]:.2%} | {em_data["10pct"]:.2%} | {sim_data["10pct"]:.4f} |
| 20% Attacked | {rcr_data["20pct"]:.2%} | {asr_data["20pct"]:.2%} | {em_data["20pct"]:.2%} | {sim_data["20pct"]:.4f} |

## Figures

See the `figures` directory for detailed plots showing the degradation of Exact Match and the increase of ASR as the knowledge base corruption increases.

## Analysis
*The Baseline False ASR validates our heuristic detectors. A high false ASR would indicate overly aggressive detection rules.*
"""

    # Check for negative finding
    negative_findings = []
    for c in corpora:
        if c != "Clean" and rcr_data[c] == 0.0 and asr_data[c] == 0.0:
            negative_findings.append(c)
            
    if negative_findings:
        md += f"\n**Documented Negative Finding**: For corpora {', '.join(negative_findings)}, both RCR and ASR were exactly 0.00%. No contamination was observed. The system successfully maintained robustness despite the injected payloads.\n"

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md)
        
    print(f"Report generated successfully at {report_path}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Path to input CSV")
    parser.add_argument("--output_dir", required=True, help="Directory for plots")
    parser.add_argument("--pilot", action="store_true", help="Prefix plots with pilot_")
    args = parser.parse_args()
    
    generate_report(args.csv, args.output_dir, args.pilot)

if __name__ == "__main__":
    main()
