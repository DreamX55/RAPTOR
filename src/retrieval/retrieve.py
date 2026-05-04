import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Default file paths
INDEX_PATH = "data/processed/faiss_index.index"
MAPPING_PATH = "data/processed/chunk_mapping.json"
MODEL_NAME = "all-MiniLM-L6-v2"

class FAISSRetriever:
    """
    A reusable module for retrieving documents from a pre-built FAISS index.
    """
    def __init__(self, index_path=INDEX_PATH, mapping_path=MAPPING_PATH, model_name=MODEL_NAME):
        print(f"Loading embedding model '{model_name}'...")
        self.model = SentenceTransformer(model_name)
        
        print(f"Loading FAISS index from '{index_path}'...")
        if not os.path.exists(index_path):
            raise FileNotFoundError(f"FAISS index not found at {index_path}. Have you built it yet?")
        self.index = faiss.read_index(index_path)
        
        print(f"Loading chunk mapping from '{mapping_path}'...")
        if not os.path.exists(mapping_path):
            raise FileNotFoundError(f"Chunk mapping not found at {mapping_path}.")
        with open(mapping_path, "r", encoding="utf-8") as f:
            self.chunk_mapping = json.load(f)
            
        print("Initialization complete.\n")

    def retrieve(self, query: str, top_k: int = 5) -> list:
        """
        Retrieves the top_k most relevant chunks for a given query.
        """
        # Convert query to embedding
        query_embedding = self.model.encode([query]).astype('float32')
        
        # Search FAISS index
        distances, indices = self.index.search(query_embedding, top_k)
        
        results = []
        for j, idx in enumerate(indices[0]):
            # FAISS can return -1 if it doesn't find enough neighbors
            if idx < len(self.chunk_mapping) and idx != -1:
                chunk = self.chunk_mapping[idx]
                results.append({
                    "rank": j + 1,
                    "score": float(distances[0][j]),  # Convert to standard float for JSON serialization
                    "chunk_id": chunk.get("chunk_id", "unknown"),
                    "source_id": chunk.get("source_id", "unknown"),
                    "text": chunk.get("text", "")
                })
                
        return results

def main():
    print("=== RAPTOR Retrieval Module ===")
    try:
        retriever = FAISSRetriever()
    except Exception as e:
        print(f"Error initializing retriever: {e}")
        print("Make sure you have run the index building script first.")
        return

    print("Type your queries below. Press Ctrl+C or type 'exit' to quit.")
    
    while True:
        try:
            query = input("\nEnter query: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            if not query:
                continue
                
            print(f"\n[Query] '{query}'")
            
            # Retrieve top 5 results
            results = retriever.retrieve(query, top_k=5)
            print(f"Retrieved {len(results)} results.\n")
            
            # Print formatted results
            for res in results:
                print(f"--- Rank {res['rank']} (Score: {res['score']:.4f}) ---")
                print(f"Chunk ID: {res['chunk_id']} | Source ID: {res['source_id']}")
                
                # Truncate text slightly for terminal readability
                text = res['text']
                snippet = text[:400] + "..." if len(text) > 400 else text
                print(f"Text:\n{snippet}\n")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
