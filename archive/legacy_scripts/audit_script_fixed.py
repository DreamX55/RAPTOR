import pandas as pd
df = pd.read_csv("reports/asr_results_targeted.csv")
targeted = df[df["is_targeted"] == True]

print(f"Total targeted evaluated: {len(targeted)}")
print(f"Total attack successes: {targeted['attack_success'].sum()}")
retrieved = targeted["retrieved_attack"] == True
successful = targeted["attack_success"] == True

print(f"Retrieved & Successful: {(retrieved & successful).sum()}")
print(f"Retrieved & Failed: {(retrieved & ~successful).sum()}")
print(f"Not Retrieved & Successful: {(~retrieved & successful).sum()}")
print(f"Not Retrieved & Failed: {(~retrieved & ~successful).sum()}")
