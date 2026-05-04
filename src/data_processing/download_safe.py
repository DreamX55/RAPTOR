import os
import sys
from itertools import islice

try:
    from datasets import load_dataset, Dataset
except ImportError:
    print("❌ Error: 'datasets' library not found.")
    print("Please run: pip install datasets==2.14.6")
    sys.exit(1)
except AttributeError as e:
    if "pyarrow" in str(e):
        print("❌ Error: Compatibility issue between 'datasets' and 'pyarrow'.")
        print("FIX: Please run: pip install 'pyarrow<15.0.0'")
    else:
        print(f"❌ Error during import: {e}")
    sys.exit(1)

# Configuration
LIMIT = 5000
BASE_DIR = "data/raw"

def safe_download_and_save(dataset_name, config, split, folder_name, limit=LIMIT):
    """
    Downloads a subset of a dataset using streaming to save space and saves it locally.
    """
    save_path = os.path.join(BASE_DIR, folder_name)
    
    # Avoid overwriting existing folders
    if os.path.exists(save_path) and any(os.scandir(save_path)):
        print(f"Skipping {folder_name}: Folder already exists and is not empty. ✅")
        return

    print(f"\n--- Processing {folder_name.upper()} ---")
    
    try:
        # Create folder
        os.makedirs(save_path, exist_ok=True)
        
        # Load with streaming to keep storage usage low
        print(f"Connecting to {dataset_name} (streaming=True)...")
        streamed_ds = load_dataset(dataset_name, config, split=split, streaming=True)
        
        # Take limited samples manually
        print(f"Fetching first {limit} samples...")
        samples = list(islice(streamed_ds, limit))
        
        if not samples:
            print(f"⚠️ Warning: No samples found for {folder_name}.")
            return
            
        # Convert the list of samples back to a Dataset object for save_to_disk
        local_ds = Dataset.from_list(samples)
        
        # Save locally
        local_ds.save_to_disk(save_path)
        print(f"Successfully saved {len(samples)} samples to {save_path} ✅")
        
    except Exception as e:
        print(f"❌ Failed to download {folder_name}: {e}")
        # Clean up empty folder if it failed
        if os.path.exists(save_path) and not any(os.scandir(save_path)):
            os.rmdir(save_path)

def main():
    print("==========================================")
    print("🚀 SAFE DATASET DOWNLOAD PIPELINE")
    print("==========================================")
    print(f"Target Directory: {os.path.abspath(BASE_DIR)}")
    
    # Define dataset sources
    tasks = [
        # UPDATED: Wikipedia fix
        {"path": "wikimedia/wikipedia", "name": "20231101.en", "split": "train", "folder": "wikipedia"},
        
        # 2. HotpotQA (fullwiki configuration)
        {"path": "hotpot_qa", "name": "fullwiki", "split": "train", "folder": "hotpotqa"},
        
        # 3. Natural Questions (nq)
        {"path": "natural_questions", "name": "default", "split": "train", "folder": "nq"},
        
        # 5. RedTeam Dataset (Anthropic HH-RLHF)
        {"path": "Anthropic/hh-rlhf", "name": "harmless-base", "split": "train", "folder": "redteam"},
    ]

    for task in tasks:
        safe_download_and_save(
            task["path"], 
            task["name"], 
            task["split"], 
            task["folder"], 
            limit=LIMIT
        )

    # UPDATED: BIPIA fix
    print("\n" + "="*42)
    print("🛠️ BIPIA DATASET INSTRUCTIONS")
    print("="*42)
    print("BIPIA cannot be loaded safely via HuggingFace.")
    print("To install BIPIA, please run the following command manually:")
    print("git clone https://github.com/microsoft/BIPIA.git data/raw/bipia")
    print("="*42)

    print("\n" + "="*42)
    print("🎉 ALL TASKS COMPLETE")
    print("Check data/raw/ for your local subsets.")
    print("="*42)

if __name__ == "__main__":
    main()