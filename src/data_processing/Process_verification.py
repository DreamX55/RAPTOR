from datasets import load_from_disk

chunks = load_from_disk("data/processed/wikipedia_chunks")

print("Total chunks:", len(chunks))
print("\nSample chunk:\n")
print(chunks[0])

