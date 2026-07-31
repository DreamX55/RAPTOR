import os
import sys
import json
import random
import argparse

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.retrieval.retrieve import FAISSRetriever

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True)
    args = parser.parse_args()
    cat = args.category
    
    print(f"Loading targeted benchmark for {cat}...")
    with open(f"data/evaluation/benchmark_{cat}.json", "r", encoding="utf-8") as f:
        benchmark_data = json.load(f)
        
    poisoned_items = [item for item in benchmark_data if item.get("poisoned_answer")]
    print(f"Total successfully poisoned items: {len(poisoned_items)}")
    
    sample_size = min(len(poisoned_items), 20)
    random.seed(42)
    sample_items = random.sample(poisoned_items, sample_size)
    
    print(f"Loading FAISS Retriever on Targeted Index for {cat}...")
    retriever = FAISSRetriever(
        index_path=f"data/processed/faiss_index_{cat}.index",
        mapping_path=f"data/processed/chunk_mapping_{cat}.json"
    )
    
    success_count = 0
    print(f"\n--- Running Retrieval Validation ({sample_size} samples) ---")
    for idx, item in enumerate(sample_items):
        results = retriever.retrieve(item["question"], top_k=3)
        target_attack_id = f"attack_doc_{cat}_{item['query_id']}"
        retrieved_ids = [res["chunk_id"] for res in results]
        
        is_success = target_attack_id in retrieved_ids
        if is_success:
            success_count += 1
            status = "✅ SUCCESS"
        else:
            status = "❌ FAILED "
            
        print(f"[{idx+1:02d}] {status} | Q: {item['question'][:60]}... | Retrieved: {retrieved_ids}")
        
    success_rate = success_count / sample_size
    print(f"\nValidation Success Rate: {success_rate:.2%} ({success_count}/{sample_size})")
    
    if success_rate >= 0.50:
        print("\n✅ RETRIEVAL VALIDATION PASSED. Proceeding to evaluation.")
        sys.exit(0)
    else:
        print("\n❌ RETRIEVAL VALIDATION FAILED. Halting pipeline.")
        sys.exit(1)

if __name__ == "__main__":
    main()
