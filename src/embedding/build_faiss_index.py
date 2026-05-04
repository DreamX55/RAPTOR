import os
import json
import numpy as np
import faiss
from datasets import load_from_disk
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def main():
    # Define paths
    dataset_path = "data/processed/wikipedia_chunks"
    index_save_path = "data/processed/faiss_index.index"
    mapping_save_path = "data/processed/chunk_mapping.json"
    
    # Load dataset
    print(f"Loading dataset from {dataset_path}...")
    try:
        dataset = load_from_disk(dataset_path)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        print("Please ensure the dataset exists at the specified path.")
        return
    
    # Initialize model
    print("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    
    # Parameters
    batch_size = 64
    embedding_dim = model.get_sentence_embedding_dimension()
    
    # Initialize FAISS index
    index = faiss.IndexFlatL2(embedding_dim)
    
    chunk_mapping = []
    
    print(f"Generating embeddings and building index for {len(dataset)} chunks...")
    
    # Process in batches
    for i in tqdm(range(0, len(dataset), batch_size), desc="Processing Batches"):
        batch = dataset[i:i + batch_size]
        texts = batch["text"]
        
        # Handle cases where chunk_id or source_id might not exist in the dataset
        chunk_ids = batch.get("chunk_id", [f"chunk_{j}" for j in range(i, i + len(texts))])
        source_ids = batch.get("source_id", ["unknown_source"] * len(texts))
        
        # Generate embeddings
        # Setting show_progress_bar=False to avoid nested progress bars
        embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=False)
        embeddings = np.array(embeddings).astype('float32')
        
        # Add to FAISS index
        index.add(embeddings)
        
        # Save mapping
        for j in range(len(texts)):
            chunk_mapping.append({
                "chunk_id": chunk_ids[j],
                "source_id": source_ids[j],
                "text": texts[j]
            })
            
    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(index_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(mapping_save_path), exist_ok=True)
    
    # Save index
    print(f"\nSaving FAISS index to {index_save_path}...")
    faiss.write_index(index, index_save_path)
    
    # Save mapping
    print(f"Saving chunk mapping to {mapping_save_path}...")
    with open(mapping_save_path, "w", encoding="utf-8") as f:
        json.dump(chunk_mapping, f, ensure_ascii=False, indent=2)
        
    # Logging
    print("\n--- Summary ---")
    print(f"Total chunks processed: {len(chunk_mapping)}")
    print(f"Embedding dimension: {embedding_dim}")
    print(f"Index size: {index.ntotal}")
    if len(chunk_mapping) > 0:
        sample_emb_shape = embeddings[0].shape
        print(f"Sample embedding shape: {sample_emb_shape}")
        
    # Optional test
    print("\n--- Running Test Query ---")
    test_query(model, index, chunk_mapping)

def test_query(model, index, chunk_mapping, query="What is artificial intelligence?"):
    print(f"Query: '{query}'")
    
    # Convert query to embedding
    query_embedding = model.encode([query]).astype('float32')
    
    # Retrieve top 3 nearest chunks
    k = 3
    distances, indices = index.search(query_embedding, k)
    
    print(f"\nTop {k} Results:")
    for j, idx in enumerate(indices[0]):
        if idx < len(chunk_mapping) and idx != -1:
            chunk = chunk_mapping[idx]
            dist = distances[0][j]
            print(f"Rank {j+1} (Distance: {dist:.4f})")
            print(f"Chunk ID: {chunk.get('chunk_id')}, Source ID: {chunk.get('source_id')}")
            
            # Print a snippet of the text
            text_snippet = chunk['text'][:200] + "..." if len(chunk['text']) > 200 else chunk['text']
            print(f"Text: {text_snippet}\n")

if __name__ == "__main__":
    main()
