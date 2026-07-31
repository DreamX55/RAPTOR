import pandas as pd
import numpy as np
import scipy.stats as stats

def calc_ci(p, n):
    if n == 0: return 0.0
    return 1.96 * np.sqrt((p * (1 - p)) / n) * 100

def chi_square_test(df_base, df_comp):
    s1 = (df_base["attack_success"].astype(str) == "True").sum()
    f1 = len(df_base) - s1
    s2 = (df_comp["attack_success"].astype(str) == "True").sum()
    f2 = len(df_comp) - s2
    
    contingency = [[s1, f1], [s2, f2]]
    chi2, p, _, _ = stats.chi2_contingency(contingency)
    return chi2, p

def main():
    cats = {
        "Instruction Injection": "reports/asr_results_instruction_injection.csv",
        "Goal Hijacking": "reports/asr_results_goal_hijacking.csv",
        "Information Extraction": "reports/asr_results_information_extraction.csv"
    }
    
    df_kp = pd.read_csv("reports/final_phase4b_extension/asr_results_targeted_extension.csv")
    df_kp_tgt = df_kp[df_kp["is_targeted"].astype(str) == "True"]
    
    out_md = "reports/phase4c_verification_audit.md"
    
    final_table = []
    
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("# Phase 4C Verification Audit\n\n")
        
        for name, path in cats.items():
            df = pd.read_csv(path)
            df_tgt = df[df["is_targeted"].astype(str) == "True"]
            
            n_targeted = len(df_tgt)
            top1_rcr = (df_tgt["retrieved_attack_top1"].astype(str) == "True").mean() * 100
            top3_rcr = (df_tgt["retrieved_attack_top3"].astype(str) == "True").mean() * 100
            
            s_ret_top3 = df_tgt["retrieved_attack_top3"].astype(str) == "True"
            s_success = df_tgt["attack_success"].astype(str) == "True"
            
            ret_succ = (s_ret_top3 & s_success).sum()
            ret_fail = (s_ret_top3 & ~s_success).sum()
            noret_succ = (~s_ret_top3 & s_success).sum()
            noret_fail = (~s_ret_top3 & ~s_success).sum()
            
            asr = s_success.mean() * 100
            asr_ci = calc_ci(asr / 100, n_targeted)
            
            sim_scores = pd.to_numeric(df_tgt["semantic_similarity"], errors="coerce")
            mean_sim = sim_scores.mean()
            
            chi2, p_val = chi_square_test(df_kp_tgt, df_tgt)
            is_sig = "Y" if p_val < 0.05 else "N"
            
            final_table.append((name, top1_rcr, top3_rcr, asr, s_success.sum()))
            
            f.write(f"## {name}\n\n")
            
            f.write("### Dataset Generation\n")
            f.write(f"* Questions selected: {n_targeted}\n")
            f.write(f"* Targeted chunks generated: {n_targeted}\n")
            f.write(f"* Targeted chunks indexed: {n_targeted}\n")
            f.write(f"* Final attack ratio: {n_targeted} / 106963 (~{(n_targeted/106963)*100:.2f}%)\n\n")
            
            f.write("### Retrieval Validation\n")
            f.write(f"* Top-1 RCR: {top1_rcr:.2f}%\n")
            f.write(f"* Top-3 RCR: {top3_rcr:.2f}%\n")
            f.write(f"* Retrieval validation success count: {s_ret_top3.sum()} / {n_targeted}\n")
            f.write(f"* Retrieval validation percentage: {top3_rcr:.2f}%\n\n")
            
            f.write("### Evaluation Metrics\n")
            f.write(f"* Questions evaluated: {len(df)}\n")
            f.write(f"* Attack successes: {s_success.sum()}\n")
            f.write(f"* ASR (%): {asr:.2f}%\n")
            f.write(f"* 95% Confidence Interval: ±{asr_ci:.2f}%\n")
            f.write(f"* Mean semantic similarity: {mean_sim:.4f}\n\n")
            
            f.write("### Statistical Significance (vs Knowledge Poisoning)\n")
            f.write(f"* Chi-square statistic: {chi2:.4f}\n")
            f.write(f"* p-value: {p_val:.4e}\n")
            f.write(f"* Significant? {is_sig}\n\n")
            
            f.write("### Confusion Matrix\n")
            f.write(f"* Retrieved & Successful: {ret_succ}\n")
            f.write(f"* Retrieved & Failed: {ret_fail}\n")
            f.write(f"* Not Retrieved & Successful: {noret_succ}\n")
            f.write(f"* Not Retrieved & Failed: {noret_fail}\n\n")
            
            f.write("### Top Examples\n\n")
            
            succ_df = df_tgt[s_success].head(5)
            fail_df = df_tgt[~s_success].head(5)
            
            f.write("#### 5 Successful Attacks\n")
            if len(succ_df) == 0:
                f.write("* No successful attacks found.\n")
            else:
                for idx, row in succ_df.iterrows():
                    f.write(f"- **Q**: {row['question']}\n")
                    f.write(f"  - **Correct Answer**: {row['correct_answer']}\n")
                    f.write(f"  - **Poison Target**: {row['poisoned_answer']}\n")
                    f.write(f"  - **Generated**: {row['generated_answer']}\n")
            f.write("\n")
            
            f.write("#### 5 Failed Attacks\n")
            if len(fail_df) == 0:
                f.write("* No failed attacks found.\n")
            else:
                for idx, row in fail_df.iterrows():
                    f.write(f"- **Q**: {row['question']}\n")
                    f.write(f"  - **Correct Answer**: {row['correct_answer']}\n")
                    f.write(f"  - **Poison Target**: {row['poisoned_answer']}\n")
                    f.write(f"  - **Generated**: {row['generated_answer']}\n")
            f.write("\n---\n\n")
            
        f.write("## Final Comparison Table\n\n")
        f.write("| Attack Type | Top-1 RCR | Top-3 RCR | ASR | Successes |\n")
        f.write("| ----------- | --------- | --------- | --- | --------- |\n")
        for name, t1, t3, asr, succ in final_table:
            f.write(f"| {name} | {t1:.2f}% | {t3:.2f}% | {asr:.2f}% | {succ} |\n")

    print("Audit generated at reports/phase4c_verification_audit.md")

if __name__ == "__main__":
    main()
