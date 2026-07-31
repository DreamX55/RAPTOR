import pandas as pd
import json
import re

df = pd.read_csv("reports/asr_results_targeted.csv")
targeted = df[df["is_targeted"] == True]
non_targeted = df[df["is_targeted"] == False]

total_targeted_evaluated = len(targeted)
total_attack_successes = targeted["attack_success"].sum()

retrieved = targeted["retrieved_attack"] == True
successful = targeted["attack_success"] == True

ret_succ = (retrieved & successful).sum()
ret_fail = (retrieved & ~successful).sum()
not_ret_succ = (~retrieved & successful).sum()
not_ret_fail = (~retrieved & ~successful).sum()

print(f"Total targeted evaluated: {total_targeted_evaluated}")
print(f"Total attack successes: {total_attack_successes}")
print(f"Retrieved & Successful: {ret_succ}")
print(f"Retrieved & Failed: {ret_fail}")
print(f"Not Retrieved & Successful: {not_ret_succ}")
print(f"Not Retrieved & Failed: {not_ret_fail}")

print("\nAttack Types:")
print(targeted[successful]["attack_type"].value_counts())

