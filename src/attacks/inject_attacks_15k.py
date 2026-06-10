import os
import random
from datasets import load_from_disk, concatenate_datasets

# Setup
random.seed(42)

CLEAN_DATA_PATH = "data/processed/wikipedia_chunks_15k"
ATTACK_DOCS_PATH = "data/processed/attack_docs"
RATIOS = [0.01, 0.05, 0.10]
RATIO_NAMES = ["1pct", "5pct", "10pct"]

print(f"Loading clean dataset from {CLEAN_DATA_PATH}...")
clean_ds = load_from_disk(CLEAN_DATA_PATH)
clean_len = len(clean_ds)
print(f"Clean dataset size: {clean_len} chunks")

print(f"Loading attack corpus from {ATTACK_DOCS_PATH}...")
attack_ds = load_from_disk(ATTACK_DOCS_PATH)
attack_len = len(attack_ds)
print(f"Attack corpus size: {attack_len} documents")

# Create injected datasets
for ratio, name in zip(RATIOS, RATIO_NAMES):
    num_attacks = int(clean_len * ratio)
    print(f"\nProcessing {name} ratio ({ratio*100}%): injecting {num_attacks} attacks...")
    
    # We may need to sample with replacement if num_attacks > attack_len
    # Randomly select indices
    selected_indices = random.choices(range(attack_len), k=num_attacks)
    
    # Select from attack dataset
    selected_attacks_ds = attack_ds.select(selected_indices)
    
    def format_attack(example, idx):
        # We also want to guarantee unique chunk_ids for the injected attacks so there are no duplicates.
        return {
            "text": example["text"],
            "chunk_id": f"{example['chunk_id']}_{idx}",
            "source_id": example["source_id"]
        }
        
    formatted_attacks = selected_attacks_ds.map(format_attack, with_indices=True, remove_columns=attack_ds.column_names)
    
    # Now concatenate
    poisoned_ds = concatenate_datasets([clean_ds, formatted_attacks])
    
    # Shuffle the dataset so attacks are distributed
    poisoned_ds = poisoned_ds.shuffle(seed=42)
    
    out_path = f"data/processed/wikipedia_chunks_15k_attacked_{name}"
    poisoned_ds.save_to_disk(out_path)
    print(f"Saved poisoned dataset to {out_path}. Total size: {len(poisoned_ds)}")

print("\nInjection complete.")
