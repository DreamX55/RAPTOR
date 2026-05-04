import os
import sys

try:
    from datasets import load_from_disk
except ImportError:
    print("❌ Error: 'datasets' library not found. Run: pip install datasets==2.14.6")
    sys.exit(1)

# Configuration
BASE_DIR = "data/raw"
HF_DATASETS = ["wikipedia", "hotpotqa", "nq", "redteam"]
BIPIA_FOLDER = "bipia"

def verify_hf_dataset(name):
    """Verifies a HuggingFace dataset saved to disk."""
    path = os.path.join(BASE_DIR, name)
    print(f"\n--- Verifying {name.upper()} ---")
    
    if not os.path.exists(path):
        print(f"❌ FAILED: Folder '{path}' does not exist.")
        return False
    
    try:
        ds = load_from_disk(path)
        length = len(ds)
        print(f"✅ SUCCESS: Loaded dataset with {length} samples.")
        
        # Print first sample preview
        print("Sample Preview:")
        first_sample = ds[0]
        # Truncate long strings for clean output
        preview = {k: (str(v)[:150] + "..." if isinstance(v, str) and len(str(v)) > 150 else v) for k, v in first_sample.items()}
        print(preview)
        return True
    except Exception as e:
        print(f"❌ FAILED: Could not load dataset. Error: {e}")
        return False

def verify_bipia():
    """Verifies the BIPIA GitHub clone by checking for data files recursively."""
    path = os.path.join(BASE_DIR, BIPIA_FOLDER)
    print(f"\n--- Verifying BIPIA ---")
    
    if not os.path.exists(path):
        print(f"❌ FAILED: Folder '{path}' does not exist.")
        return False
    
    try:
        # Recursive search for data files
        data_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(('.json', '.jsonl', '.parquet', '.csv')):
                    data_files.append(os.path.join(root, file))
        
        if len(data_files) > 0:
            print(f"✅ SUCCESS: Folder exists and contains {len(data_files)} data files.")
            print(f"Sample data files found:")
            for f in data_files[:5]:
                print(f"  - {os.path.relpath(f, path)}")
            return True
        else:
            print("❌ FAILED: No JSON or data files found in the repository.")
            return False
    except Exception as e:
        print(f"❌ FAILED: Error checking folder. Error: {e}")
        return False

def main():
    print("==========================================")
    print("🔍 RAPTOR DATASET VALIDATION")
    print("==========================================")
    
    success_count = 0
    total_datasets = len(HF_DATASETS) + 1 # +1 for BIPIA
    
    # Verify HF Datasets
    for name in HF_DATASETS:
        if verify_hf_dataset(name):
            success_count += 1
            
    # Verify BIPIA
    if verify_bipia():
        success_count += 1
        
    # Final Summary
    print("\n" + "="*42)
    print("📊 VALIDATION SUMMARY")
    print("="*42)
    print(f"Total Datasets: {total_datasets}")
    print(f"Successful:     {success_count}")
    print(f"Failed:         {total_datasets - success_count}")
    
    if success_count == total_datasets:
        print("\n✨ ALL DATASETS ARE CORRECTLY STORED! Ready for RAPTOR development.")
    else:
        print("\n⚠️ SOME DATASETS FAILED VALIDATION. Please check the errors above.")
    print("="*42)

if __name__ == "__main__":
    main()
