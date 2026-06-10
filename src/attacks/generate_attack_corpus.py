import json
import glob
import os
import random
import uuid
from datasets import Dataset

# Setup random seed for reproducibility
random.seed(42)

# Define categories
TARGET_CATEGORIES = [
    "Malware Distribution", 
    "Clickbait", 
    "Persuasion", 
    "Alphanumeric Substitution"
]

# Load original prompts
print("Loading BIPIA prompts...")
bipia_files = glob.glob("data/raw/bipia/benchmark/*_attack_*.json")
original_prompts = {cat: [] for cat in TARGET_CATEGORIES}

for fpath in bipia_files:
    with open(fpath, "r") as f:
        data = json.load(f)
        for cat in TARGET_CATEGORIES:
            if cat in data:
                original_prompts[cat].extend(data[cat])

for cat in TARGET_CATEGORIES:
    original_prompts[cat] = list(set(original_prompts[cat]))  # Deduplicate just in case
    print(f"Found {len(original_prompts[cat])} unique base prompts for {cat}")

# Procedural generation templates
CONTEXT_PREFIXES = [
    "The following section describes the history of the event. ",
    "A notable controversy emerged during this period. ",
    "Researchers have recently pointed out that ",
    "In a widely circulated report, it was noted: ",
    "Critics argue that the implementation was flawed. ",
    "Further investigation revealed additional details. ",
    "According to contemporary sources, ",
    "An interesting footnote to this phenomenon is that ",
    "Moreover, experts have suggested that ",
    "It is also important to consider the broader context. "
]

CONTEXT_SUFFIXES = [
    " This ultimately led to widespread changes.",
    " The impact of these events is still debated today.",
    " Several scholars disagree with this interpretation.",
    " This remains a highly controversial topic.",
    " More research is needed to fully understand the implications.",
    " However, public opinion varied significantly.",
    " The long-term effects were immediately apparent.",
    " This theory has since been largely discredited.",
    " Ultimately, the decision was reversed.",
    " Many consider this to be a turning point."
]

FORMAT_WRAPPERS = [
    ("### Historical Context\n", "\n\n*References available upon request.*"),
    ("#### Key Findings:\n- ", "\n- End of summary."),
    ("Overview:\n", ""),
    ("1. Introduction\n", "\n2. Conclusion"),
    ("> Note: ", ""),
    ("Summary: ", "\n(Source: Archive)"),
    ("Abstract - ", "\nKeywords: history, debate.")
]

# Paraphrasing dictionary for simple synonym replacement (to increase uniqueness without LLM)
SYNONYMS = {
    "Add": ["Include", "Insert", "Append", "Incorporate"],
    "response": ["answer", "reply", "output", "message"],
    "reply": ["answer", "response", "output", "message"],
    "Modify": ["Alter", "Change", "Adjust", "Update"],
    "Integrate": ["Embed", "Include", "Add", "Incorporate"],
    "users": ["readers", "visitors", "individuals", "people"],
    "answer": ["response", "reply", "explanation", "output"],
    "Provide": ["Give", "Supply", "Offer", "Deliver"],
}

def paraphrase(prompt):
    words = prompt.split()
    new_words = []
    for w in words:
        clean_w = w.strip(".,!?:;'\"")
        if clean_w in SYNONYMS and random.random() > 0.5:
            replacement = random.choice(SYNONYMS[clean_w])
            # Preserve case if it was capitalized
            if w[0].isupper():
                replacement = replacement.capitalize()
            # Restore punctuation
            if w.endswith((".", ",", "!", "?", ":", ";")):
                replacement += w[-1]
            new_words.append(replacement)
        else:
            new_words.append(w)
    return " ".join(new_words)

# Generate corpus
generated_docs = []

print("Generating 1000 attack documents...")
for cat in TARGET_CATEGORIES:
    base_prompts = original_prompts[cat]
    if not base_prompts:
        print(f"Warning: No base prompts found for {cat}")
        continue
        
    for i in range(250):
        base_prompt = random.choice(base_prompts)
        para_prompt = paraphrase(base_prompt)
        
        prefix = random.choice(CONTEXT_PREFIXES)
        suffix = random.choice(CONTEXT_SUFFIXES)
        wrapper_start, wrapper_end = random.choice(FORMAT_WRAPPERS)
        
        # Combine into realistic looking document
        final_text = f"{wrapper_start}{prefix}{para_prompt}{suffix}{wrapper_end}"
        
        generated_docs.append({
            "text": final_text,
            "chunk_id": f"attack_doc_{cat[:3].lower()}_{uuid.uuid4().hex[:8]}",
            "source_id": "bipia_generated",
            "attack_category": cat,
            "original_prompt": base_prompt
        })

print(f"Generated {len(generated_docs)} total documents.")

# Save as HuggingFace Dataset
ds = Dataset.from_list(generated_docs)
output_dir = "data/processed/attack_docs"
os.makedirs(output_dir, exist_ok=True)
ds.save_to_disk(output_dir)

print(f"Attack corpus saved to {output_dir}")
