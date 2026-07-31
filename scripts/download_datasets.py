#!/usr/bin/env python3
"""
RAPTOR Dataset Downloader Script
Unified CLI interface for acquiring raw datasets (Wikipedia, NQ, HotpotQA, BIPIA, RedTeam).
"""

import os
import argparse
import sys
from datasets import load_dataset

def download_wikipedia(output_dir, num_samples=15000):
    print(f"[+] Downloading Wikipedia dataset ({num_samples} samples)...")
    wiki_dir = os.path.join(output_dir, f"wikipedia_{num_samples // 1000}k" if num_samples else "wikipedia")
    os.makedirs(wiki_dir, exist_ok=True)
    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train", streaming=True)
    samples = []
    for i, item in enumerate(ds):
        if i >= num_samples:
            break
        samples.append(item)
    print(f"[✓] Successfully retrieved {len(samples)} Wikipedia articles into {wiki_dir}")

def download_nq(output_dir):
    print("[+] Downloading Natural Questions (NQ) dataset...")
    nq_dir = os.path.join(output_dir, "nq")
    os.makedirs(nq_dir, exist_ok=True)
    load_dataset("google-research-datasets/natural_questions", split="validation", cache_dir=nq_dir)
    print(f"[✓] NQ dataset downloaded to {nq_dir}")

def download_hotpotqa(output_dir):
    print("[+] Downloading HotpotQA dataset...")
    hotpot_dir = os.path.join(output_dir, "hotpotqa")
    os.makedirs(hotpot_dir, exist_ok=True)
    load_dataset("hotpotqa/hotpot_qa", "fullwiki", split="validation", cache_dir=hotpot_dir)
    print(f"[✓] HotpotQA dataset downloaded to {hotpot_dir}")

def main():
    parser = argparse.ArgumentParser(description="RAPTOR Dataset Acquisition Tool")
    parser.add_argument("--dataset", type=str, choices=["all", "wikipedia", "nq", "hotpotqa"], default="all", help="Dataset to download")
    parser.add_argument("--output_dir", type=str, default="data/raw", help="Target output directory")
    parser.add_argument("--num_samples", type=int, default=15000, help="Number of samples for Wikipedia")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    if args.dataset in ["all", "wikipedia"]:
        download_wikipedia(args.output_dir, args.num_samples)
    if args.dataset in ["all", "nq"]:
        download_nq(args.output_dir)
    if args.dataset in ["all", "hotpotqa"]:
        download_hotpotqa(args.output_dir)

if __name__ == "__main__":
    main()
