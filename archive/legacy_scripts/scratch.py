from datasets import load_from_disk
ds = load_from_disk("data/processed/attack_docs")
print("Features:", ds.features)
print("First 3 attacks:")
for i in range(3):
    print(ds[i])
