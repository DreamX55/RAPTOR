import os
from datasets import load_dataset

# =========================
# Create folder structure
# =========================
folders = [
    "data/raw/nq",
    "data/raw/hotpotqa",
    "data/raw/wikipedia",
    "data/raw/redteam",
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

print("Folders created ✅")

# =========================
# 1. Natural Questions
# =========================
print("\nDownloading Natural Questions...")
nq = load_dataset("natural_questions", split="train[:5000]")  # small subset first
nq.save_to_disk("data/raw/nq")
print("NQ done ✅")

# =========================
# 2. HotpotQA
# =========================
print("\nDownloading HotpotQA...")
hotpot = load_dataset("hotpot_qa", "fullwiki", split="train[:10000]")
hotpot.save_to_disk("data/raw/hotpotqa")
print("HotpotQA done ✅")

# =========================
# 3. Wikipedia (DPR version)
# =========================
print("\nDownloading Wikipedia corpus...")
wiki = load_dataset("wiki_dpr", "psgs_w100", split="train[:50000]")
wiki.save_to_disk("data/raw/wikipedia")
print("Wikipedia done ✅")

# =========================
# 4. Agentic RedTeam
# =========================
print("\nDownloading RedTeam dataset...")
redteam = load_dataset("Fujitsu/agentic-rag-redteam-bench", split="train[:5000]")
redteam.save_to_disk("data/raw/redteam")
print("RedTeam done ✅")

print("\n🎉 ALL DATASETS DOWNLOADED SUCCESSFULLY!")