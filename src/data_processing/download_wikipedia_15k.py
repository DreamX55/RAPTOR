import os
import sys
from itertools import islice

try:
    from datasets import load_dataset, Dataset
except ImportError:
    print("❌ Error: 'datasets' library not found.")
    sys.exit(1)

LIMIT = 15000
BASE_DIR = "data/raw"
FOLDER_NAME = "wikipedia_15k"

def main():
    save_path = os.path.join(BASE_DIR, FOLDER_NAME)
    
    if os.path.exists(save_path) and any(os.scandir(save_path)):
        print(f"Skipping {FOLDER_NAME}: Folder already exists and is not empty. ✅")
        return

    print(f"\n--- Processing {FOLDER_NAME.upper()} ---")
    
    try:
        os.makedirs(save_path, exist_ok=True)
        print("Connecting to wikimedia/wikipedia (streaming=True)...")
        streamed_ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)
        
        print(f"Fetching first {LIMIT} samples...")
        samples = list(islice(streamed_ds, LIMIT))
        
        local_ds = Dataset.from_list(samples)
        local_ds.save_to_disk(save_path)
        print(f"Successfully saved {len(samples)} samples to {save_path} ✅")
        
    except Exception as e:
        print(f"❌ Failed to download {FOLDER_NAME}: {e}")
        if os.path.exists(save_path) and not any(os.scandir(save_path)):
            os.rmdir(save_path)

if __name__ == "__main__":
    main()
