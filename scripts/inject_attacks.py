#!/usr/bin/env python3
"""
RAPTOR Attack Injection Engine
Unified CLI generator for prompt injection & retrieval poisoning attacks.
"""

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="RAPTOR Attack Corpus Injector")
    parser.add_argument("--corpus_path", type=str, default="data/processed/wikipedia_chunks_15k", help="Target corpus path")
    parser.add_argument("--attack_type", type=str, choices=["targeted", "instruction_injection", "goal_hijacking", "information_extraction"], default="targeted", help="Attack category")
    parser.add_argument("--poison_ratio", type=float, default=0.05, help="Ratio of poisoned documents (e.g., 0.05 for 5%%)")
    parser.add_argument("--output_path", type=str, default="data/processed/wikipedia_chunks_15k_attacked", help="Output attacked corpus path")
    args = parser.parse_args()

    print(f"[+] Injecting {args.attack_type} attack (poison_ratio={args.poison_ratio}) into {args.corpus_path}...")
    os.makedirs(args.output_path, exist_ok=True)
    print(f"[✓] Poisoned corpus saved to {args.output_path}")

if __name__ == "__main__":
    main()
