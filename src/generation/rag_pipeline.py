import sys
import os
import requests

# Add project root to sys.path to allow absolute imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.retrieval.retrieve import FAISSRetriever

# 1. Load the retrieval module
print("Initializing FAISS Retriever...")
try:
    retriever = FAISSRetriever()
except Exception as e:
    print(f"Failed to initialize retriever: {e}")
    sys.exit(1)

print("Pipeline initialization complete.\n")

def generate_answer(query: str):
    """
    Retrieves context for a query and generates an answer using Ollama (Mistral).
    """
    # Call retrieve(query, top_k=2)
    results = retriever.retrieve(query, top_k=2)
    
    # Limit each chunk to first ~150 words
    processed_contexts = []
    for res in results:
        words = res["text"].split()
        truncated_text = " ".join(words[:150])
        processed_contexts.append(truncated_text)
        
    # Combine retrieved text into context
    context = "\n\n".join(processed_contexts)
    
    # Format prompt
    prompt = f"""You are a helpful assistant.
Answer the question based only on the context below.

Context:
{context}

Question:
{query}

Give a clear and complete answer."""

    # 2. Ollama API call
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        final_answer = response.json().get("response", "").strip()
    except requests.exceptions.ConnectionError:
        print("\n[WARNING] Could not connect to Ollama.")
        print("Please ensure Ollama is running locally (e.g., 'ollama serve' or open the Ollama app).")
        final_answer = "Error: Ollama connection failed."
    except Exception as e:
        print(f"\n[WARNING] Error communicating with Ollama API: {e}")
        final_answer = f"Error: {e}"
            
    return final_answer, results

def main():
    print("=== RAPTOR Full RAG Pipeline (Ollama / Mistral) ===")
    print("Type your queries below. Press Ctrl+C or type 'exit' to quit.")
    
    while True:
        try:
            query = input("\nEnter query: ").strip()
            if query.lower() in ['exit', 'quit']:
                break
            if not query:
                continue
                
            print(f"\n[Query] '{query}'")
            
            # Generate answer
            answer, retrieved_chunks = generate_answer(query)
            
            # Print retrieved chunks
            print("\n--- Retrieved Context (Top 2) ---")
            for res in retrieved_chunks:
                # Truncate for display
                text = res['text']
                snippet = text[:200] + "..." if len(text) > 200 else text
                print(f"[Rank {res['rank']} | Chunk: {res['chunk_id']}] {snippet}")
            
            # Print final answer
            print("\n================ FINAL ANSWER ================")
            print(answer)
            print("==============================================\n")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
