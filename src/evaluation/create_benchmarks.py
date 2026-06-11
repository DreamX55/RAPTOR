import os
import json
import random
from datasets import load_from_disk

# Set seed
random.seed(42)

def create_benchmark(nq_ds, hp_ds, num_samples, output_path):
    # Sample from each dataset
    half = num_samples // 2
    
    nq_indices = random.sample(range(len(nq_ds)), half)
    hp_indices = random.sample(range(len(hp_ds)), half)
    
    benchmark = []
    
    # Process NQ
    for idx in nq_indices:
        sample = nq_ds[idx]
        q_text = sample["question"]["text"] if isinstance(sample["question"], dict) else sample["question"]
        benchmark.append({
            "query_id": f"nq_{sample['id']}" if 'id' in sample else f"nq_{idx}",
            "question": q_text,
            "answer": sample["answers"][0] if isinstance(sample.get("answers"), list) and len(sample["answers"]) > 0 else sample.get("answer", ""),
            "dataset_source": "nq"
        })
        
    # Process HotpotQA
    for idx in hp_indices:
        sample = hp_ds[idx]
        q_text = sample["question"]["text"] if isinstance(sample["question"], dict) else sample["question"]
        benchmark.append({
            "query_id": f"hp_{sample['id']}" if 'id' in sample else f"hp_{idx}",
            "question": q_text,
            "answer": sample["answer"] if "answer" in sample else "",
            "dataset_source": "hotpotqa"
        })
        
    # Shuffle the final benchmark
    random.shuffle(benchmark)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(benchmark, f, indent=2)
        
    print(f"Saved {len(benchmark)} questions to {output_path}")

def main():
    print("Loading datasets...")
    # These paths are based on typical RAPTOR structure, assuming data is in HF arrow format
    nq_path = "data/raw/nq"
    hp_path = "data/raw/hotpotqa"
    
    if not os.path.exists(nq_path) or not os.path.exists(hp_path):
        print("Raw datasets not found. Please ensure data/raw/nq and data/raw/hotpotqa exist.")
        return
        
    nq_ds = load_from_disk(nq_path)
    hp_ds = load_from_disk(hp_path)
    
    print(f"Loaded NQ: {len(nq_ds)} samples")
    print(f"Loaded HotpotQA: {len(hp_ds)} samples")
    
    os.makedirs("data/evaluation", exist_ok=True)
    
    print("\nCreating Pilot Benchmark (100 samples)...")
    create_benchmark(nq_ds, hp_ds, 100, "data/evaluation/benchmark_100.json")
    
    print("Creating Full Benchmark (2000 samples)...")
    create_benchmark(nq_ds, hp_ds, 2000, "data/evaluation/benchmark_2000.json")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
