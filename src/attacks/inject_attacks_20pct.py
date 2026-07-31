import os
import random
import gc
from datasets import load_from_disk, concatenate_datasets

# Setup
random.seed(42)

CLEAN_DATA_PATH = "data/processed/wikipedia_chunks_15k"
ATTACK_DOCS_PATH = "data/processed/attack_docs"
RATIO = 0.20
RATIO_NAME = "20pct"

print(f"Loading clean dataset from {CLEAN_DATA_PATH}...")
clean_ds = load_from_disk(CLEAN_DATA_PATH)
clean_len = len(clean_ds)
print(f"Clean dataset size: {clean_len} chunks")

print(f"Loading attack corpus from {ATTACK_DOCS_PATH}...")
attack_ds = load_from_disk(ATTACK_DOCS_PATH)
attack_len = len(attack_ds)
print(f"Attack corpus size: {attack_len} documents")

num_attacks = int(clean_len * RATIO)
print(f"\nProcessing {RATIO_NAME} ratio ({RATIO*100}%): injecting {num_attacks} attacks...")

# Randomly select indices (with replacement since num_attacks > attack_len)
selected_indices = random.choices(range(attack_len), k=num_attacks)

# Select from attack dataset
selected_attacks_ds = attack_ds.select(selected_indices)

def format_attack(example, idx):
    # Guarantee unique chunk_ids for the injected attacks so there are no duplicates.
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

out_path = f"data/processed/wikipedia_chunks_15k_attacked_{RATIO_NAME}"
poisoned_ds.save_to_disk(out_path)
print(f"Saved poisoned dataset to {out_path}. Total size: {len(poisoned_ds)}")

# Explicit cleanup for memory limits
del clean_ds, attack_ds, selected_attacks_ds, formatted_attacks, poisoned_ds
gc.collect()

print("\nInjection complete.")
