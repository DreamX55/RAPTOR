import os
import json
import glob

print("Running BIPIA Analysis...")

# Task 1: Dataset Exploration
bipia_dir = "data/raw/bipia"
benchmark_dir = os.path.join(bipia_dir, "benchmark")
attack_files = glob.glob(os.path.join(benchmark_dir, "*_attack_train.json")) + glob.glob(os.path.join(benchmark_dir, "*_attack_test.json"))

total_samples = 0
train_samples = 0
test_samples = 0

taxonomy = {}

for file in attack_files:
    file_size = os.path.getsize(file)
    with open(file, 'r') as f:
        data = json.load(f)
    
    is_train = "train" in file
    
    for category, examples in data.items():
        if category not in taxonomy:
            taxonomy[category] = {
                "examples": examples[:5],
                "total": 0
            }
        taxonomy[category]["total"] += len(examples)
        total_samples += len(examples)
        if is_train:
            train_samples += len(examples)
        else:
            test_samples += len(examples)

# Create the report content
report = f"""# BIPIA Dataset Analysis Report

## 1. Executive Summary
This report analyzes the BIPIA (Benchmarking Indirect Prompt Injection Attacks) dataset to inform the attack strategy for the RAPTOR RAG pipeline. It outlines the dataset structure, attack taxonomy, and provides recommendations for establishing a robust injection benchmark.

## 2. Dataset Exploration
- **Path**: `data/raw/bipia`
- **Format**: JSON configuration files mapped to python builder scripts (`bipia/data/`).
- **Total Attack Prompts Available**: {total_samples}
- **Train Split**: {train_samples}
- **Test Split**: {test_samples}

## 3. Attack Taxonomy & Examples
The BIPIA dataset provides a wide array of attack prompts, categorized by their intended behaviors. 

"""

for cat, info in taxonomy.items():
    cat_samples = info["total"]
    examples = info["examples"]
    
    # Infer Objective & Mechanism
    if "Substitution" in cat or "Misspelling" in cat or "Anagramming" in cat or "Removal" in cat:
        objective = "Bypass detection and retrieval filters via obfuscation."
        mechanism = "Modifying the syntax of the prompt to evade simple keyword-based defenses while retaining semantic intent."
        raptor_target = "Retrieval"
        failure_mode = "The retrieval system fails to filter out the malicious text, allowing it into the context window."
    elif "Information Retrieval" in cat or "Content Creation" in cat or "Tutoring" in cat or "Translation" in cat or "Programming" in cat:
        objective = "Goal Hijacking / Task Deviation."
        mechanism = "Replacing the original user task with a completely new benign task."
        raptor_target = "Generation"
        failure_mode = "The LLM ignores the user's actual question and instead answers the injected prompt (e.g., translates text or writes a poem)."
    else:
        objective = "Instruction Injection / Malicious Action."
        mechanism = "Injecting payloads that persuade the user, distribute malware, or solicit engagement."
        raptor_target = "Generation"
        failure_mode = "The LLM integrates the malicious instruction seamlessly into its final response (e.g., providing a phishing link)."

    report += f"""### Category: {cat}
- **Number of Samples**: {cat_samples}
- **Attack Objective**: {objective}
- **Attack Mechanism**: {mechanism}

**Representative Examples:**
"""
    for ex in examples:
        report += f"1. \"{ex}\"\n"
    
    report += f"""
**RAPTOR Integration & Mapping:**
- **Injected Into**: Wikipedia context chunks.
- **Targets**: {raptor_target} Phase.
- **Expected Failure Mode**: {failure_mode}

"""

report += """
## 4. RAPTOR Integration Strategy
In the RAPTOR system, attacks will be injected directly into the retrieved text chunks (simulating a poisoned Wikipedia article). 
- If the attack is an **obfuscation**, the goal is to see if our future retrieval defenses fail.
- If the attack is an **instruction injection**, the goal is to see if Mistral succumbs to the injected command over the user's prompt.

## 5. Recommendations & Research Design
To create a statistically meaningful attack benchmark without over-indexing on redundant obfuscation techniques, we recommend:

1. **Select 4 Core Attack Categories**: 
   - *Malware Distribution* (High Risk Payload)
   - *Clickbait* (Phishing/Spam)
   - *Persuasion* (Misinformation)
   - *Alphanumeric Substitution* (Obfuscation Test)
2. **Sample Counts**: Extract 50 unique attack payloads per category.
3. **Injection Ratio**: Inject attacks into 5% of the total dataset (approx. 250 poisoned chunks) to simulate a realistic poisoning scenario where only a fraction of the knowledge base is compromised.

---
*Analysis completed automatically via baseline exploration scripts.*
"""

os.makedirs("reports", exist_ok=True)
with open("reports/bipia_analysis.md", "w") as f:
    f.write(report)

print("Report generated successfully.")
