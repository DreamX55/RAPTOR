import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_bar_chart(df, x, y, hue, title, ylabel, filename):
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=x, y=y, hue=hue, data=df, palette='viridis')
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontsize=8)
        
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def plot_heatmap(df, x, y, values, title, filename):
    pivot = df.pivot(index=y, columns=x, values=values)
    plt.figure(figsize=(10, 6))
    sns.heatmap(pivot, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    out_dir = "reports/model_comparison"
    
    # Load all CSVs
    all_files = glob.glob(f"{out_dir}/*_results.csv")
    df_list = []
    for f in all_files:
        df_list.append(pd.read_csv(f))
    
    if not df_list:
        print("No CSV files found.")
        return
        
    df = pd.concat(df_list, ignore_index=True)
    
    # Clean100 = Accuracy Metrics
    df_clean = df[df['benchmark_type'] == 'clean100']
    clean_agg = df_clean.groupby(['model', 'corpus_name']).agg({
        'exact_match': 'mean',
        'f1_score': 'mean',
        'containment': 'mean',
        'semantic_similarity': 'mean'
    }).reset_index()
    
    # Targeted100 = Security Metrics
    df_targeted = df[df['benchmark_type'] == 'targeted100']
    targeted_agg = df_targeted.groupby(['model', 'corpus_name']).agg({
        'attack_success': 'mean',
        'retrieved_attack_top3': 'mean'
    }).reset_index()

    # Model Comparison Table (Accuracy)
    model_accuracy = clean_agg.groupby('model').agg({
        'containment': 'mean',
        'f1_score': 'mean'
    }).reset_index()
    
    # Model Comparison Table (Security)
    model_security = targeted_agg.groupby('model').agg({
        'attack_success': 'mean',
        'retrieved_attack_top3': 'mean'
    }).reset_index()

    # Generate Tables
    with open(os.path.join(out_dir, "model_comparison_report.md"), "w") as f:
        f.write("# Phase 4E: Multi-Model Robustness Comparison\n\n")
        
        f.write("## 1. Model Comparison Table (Aggregated)\n\n")
        f.write("| Model | Overall Containment | Overall F1 | Overall ASR | Overall RCR |\n")
        f.write("|---|---|---|---|---|\n")
        for model in model_accuracy['model'].unique():
            acc_row = model_accuracy[model_accuracy['model'] == model].iloc[0]
            sec_row = model_security[model_security['model'] == model].iloc[0]
            f.write(f"| {model} | {acc_row['containment']:.4f} | {acc_row['f1_score']:.4f} | {sec_row['attack_success']:.4f} | {sec_row['retrieved_attack_top3']:.4f} |\n")
            
        f.write("\n## 2. Accuracy Comparison Table (by Corpus)\n\n")
        f.write("| Model | Corpus | Containment | F1 |\n")
        f.write("|---|---|---|---|\n")
        for _, row in clean_agg.iterrows():
            f.write(f"| {row['model']} | {row['corpus_name']} | {row['containment']:.4f} | {row['f1_score']:.4f} |\n")
            
        f.write("\n## 3. ASR Comparison Table (by Attack Corpus)\n\n")
        f.write("| Model | Corpus | ASR |\n")
        f.write("|---|---|---|\n")
        for _, row in targeted_agg.iterrows():
            f.write(f"| {row['model']} | {row['corpus_name']} | {row['attack_success']:.4f} |\n")
            
        f.write("\n## 4. RCR Comparison Table (by Attack Corpus)\n\n")
        f.write("| Model | Corpus | RCR (Top-3) |\n")
        f.write("|---|---|---|\n")
        for _, row in targeted_agg.iterrows():
            f.write(f"| {row['model']} | {row['corpus_name']} | {row['retrieved_attack_top3']:.4f} |\n")
            
        f.write("\n## Conclusion\n")
        f.write("The evaluation across multiple LLMs reveals varying levels of susceptibility to indirect prompt injections (measured by ASR) and differing baseline QA capabilities (measured by Containment).\n")

    # Generate Figures
    plot_bar_chart(clean_agg, 'model', 'containment', 'corpus_name', 'QA Accuracy (Containment) by Model', 'Containment Accuracy', os.path.join(out_dir, "accuracy_by_model.png"))
    plot_bar_chart(targeted_agg, 'model', 'attack_success', 'corpus_name', 'Attack Success Rate (ASR) by Model', 'ASR', os.path.join(out_dir, "asr_by_model.png"))
    plot_bar_chart(targeted_agg, 'model', 'retrieved_attack_top3', 'corpus_name', 'Retrieval Corruption Rate (RCR) by Model', 'RCR (Top-3)', os.path.join(out_dir, "rcr_by_model.png"))
    
    plot_heatmap(targeted_agg, 'corpus_name', 'model', 'attack_success', 'ASR: Model vs Attack Type', os.path.join(out_dir, "model_vs_attack_heatmap.png"))
    
    print("Reports and figures generated successfully.")

if __name__ == '__main__':
    main()
