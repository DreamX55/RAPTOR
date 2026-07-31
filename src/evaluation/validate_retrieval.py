import os
import sys
import json
import random
import psutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.retrieval.retrieve import FAISSRetriever

peak_ram = 0
peak_swap = 0

def update_peaks():
    global peak_ram, peak_swap
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    peak_ram = max(peak_ram, mem.used / (1024**3))
    peak_swap = max(peak_swap, swap.used / (1024**3))

def main():
    update_peaks()
    print("Loading targeted benchmark...")
    with open("data/evaluation/benchmark_targeted_extension.json", "r", encoding="utf-8") as f:
        benchmark_data = json.load(f)
        
    # Filter only the ones that were successfully poisoned
    poisoned_items = [item for item in benchmark_data if item.get("poisoned_answer")]
    print(f"Total successfully poisoned items: {len(poisoned_items)}")
    
    if len(poisoned_items) < 20:
        sample_size = len(poisoned_items)
    else:
        sample_size = 20
        
    random.seed(42)
    sample_items = random.sample(poisoned_items, sample_size)
    
    update_peaks()
    print("Loading FAISS Retriever on Targeted Index...")
    retriever = FAISSRetriever(
        index_path="data/processed/faiss_index_targeted_extension.index",
        mapping_path="data/processed/chunk_mapping_targeted_extension.json"
    )
    
    success_count = 0
    print(f"\n--- Running Retrieval Validation ({sample_size} samples) ---")
    
    update_peaks()
    for idx, item in enumerate(sample_items):
        results = retriever.retrieve(item["question"], top_k=3)
        
        # Check if the specifically targeted attack doc for this query is retrieved
        target_attack_id = f"attack_doc_targeted_{item['query_id']}"
        retrieved_ids = [res["chunk_id"] for res in results]
        
        # A more relaxed check: any targeted attack doc, but preferably the specific one.
        is_success = target_attack_id in retrieved_ids
        
        if is_success:
            success_count += 1
            status = "✅ SUCCESS"
        else:
            status = "❌ FAILED "
            
        print(f"[{idx+1:02d}] {status} | Q: {item['question'][:60]}... | Retrieved: {retrieved_ids}")
        update_peaks()
        
    success_rate = success_count / sample_size
    print(f"\nValidation Success Rate: {success_rate:.2%} ({success_count}/{sample_size})")
    
    # Write Memory Profile
    mem_path = "reports/memory_profile_phase4b_extension.md"
    mode = "a" if os.path.exists(mem_path) else "w"
    with open(mem_path, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write("# Memory Profile: Phase 4B Extension\n\n")
        f.write("## 2. Validation Pipeline\n")
        f.write(f"- **Peak RAM**: {peak_ram:.2f} GB\n")
        f.write(f"- **Peak Swap**: {peak_swap:.2f} GB\n\n")
    
    if success_rate >= 0.50:
        print("\n✅ RETRIEVAL VALIDATION PASSED. Proceeding to evaluation.")
        sys.exit(0)
    else:
        print("\n❌ RETRIEVAL VALIDATION FAILED. Halting pipeline.")
        sys.exit(1)

if __name__ == "__main__":
    main()
