import os
import json
import glob

print("Starting BIPIA Verification...")

bipia_dir = "data/raw/bipia/benchmark"
attack_files = sorted(glob.glob(os.path.join(bipia_dir, "*_attack_*.json")))

report = """# BIPIA Dataset Verification Audit

## 1. Executive Summary
This document provides a precise, ground-truth verification of the BIPIA dataset directly from the raw attack configuration files in `data/raw/bipia/benchmark`.

## 2. Exact File Names and Sample Counts
"""

total_train_samples = 0
total_test_samples = 0
total_overall_samples = 0

all_categories = set()

file_breakdown = ""

for file_path in attack_files:
    file_name = os.path.basename(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    is_train = "train" in file_name.lower()
    
    file_samples = 0
    file_categories = list(data.keys())
    for cat in file_categories:
        all_categories.add(cat)
        file_samples += len(data[cat])
        
    total_overall_samples += file_samples
    if is_train:
        total_train_samples += file_samples
    else:
        total_test_samples += file_samples

    file_breakdown += f"- **{file_name}**: {file_samples} samples\n"

report += file_breakdown
report += f"""
### Summary Counts
- **Total Train Samples**: {total_train_samples}
- **Total Test Samples**: {total_test_samples}
- **Total Exact Sample Count**: {total_overall_samples}

## 3. Exact Category Labels (Unmodified)
The following categories exist exactly as written in the source JSON files:
"""

for cat in sorted(list(all_categories)):
    report += f"- {cat}\n"

report += f"""
## 4. Verification of Previous Report Accuracy
- **Inconsistent Total Sample Count**: The previous analysis reported 1,350 total samples. The exact verified count is {total_overall_samples}.
- **Inconsistent Train/Test Split**: The previous report stated 1,350 total attack prompts without exact train/test sizes. The exact verified splits are Train = {total_train_samples}, Test = {total_test_samples}.
- **Inconsistent Category Definitions**: The previous report summarized categories and introduced assumptions (e.g., grouping into "Instruction Injection" or "Obfuscation Attacks"). This audit extracts only the {len(all_categories)} precise, unmodified categories from the JSON schemas.

"""

os.makedirs("reports", exist_ok=True)
with open("reports/bipia_verification.md", "w", encoding="utf-8") as f:
    f.write(report)

print("Verification complete.")
