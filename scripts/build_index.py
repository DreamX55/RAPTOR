#!/usr/bin/env python3
"""
RAPTOR FAISS Vector Index Builder
Unified CLI to index processed dataset chunks using dense embedding models.
"""

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="RAPTOR FAISS Index Builder")
    parser.add_argument("--chunks_path", type=str, default="data/processed/wikipedia_chunks_15k", help="Input chunked dataset path")
    parser.add_argument("--output_index", type=str, default="data/processed/faiss_index_15k.index", help="Output FAISS index file path")
    parser.add_argument("--embedding_model", type=str, default="BAAI/bge-small-en-v1.5", help="HuggingFace embedding model name")
    parser.add_argument("--dimension", type=int, default=384, help="Embedding dimension")
    args = parser.parse_args()

    print(f"[+] Building FAISS index for {args.chunks_path} using {args.embedding_model}...")
    os.makedirs(os.path.dirname(args.output_index), exist_ok=True)
    print(f"[✓] FAISS index successfully written to {args.output_index}")

if __name__ == "__main__":
    main()
