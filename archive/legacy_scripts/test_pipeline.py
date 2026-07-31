import sys
import os

# Append current directory to path
sys.path.append(os.getcwd())

from src.ragshield.pipeline import RAGShieldRetriever

def main():
    try:
        retriever = RAGShieldRetriever()
        chunks = retriever.retrieve("What is the capital of France?", top_k=2)
        print("Success!")
        print(f"Retrieved {len(chunks)} chunks.")
    except Exception as e:
        print("Failed!", str(e))

if __name__ == '__main__':
    main()
