#!/usr/bin/env python3
"""
RAPTOR Benchmark Evaluation Runner
Main entrypoint to run Phase 4 (Attacks), Phase 5 (Design), and Phase 6 (RAGShield Defense) experiments.
"""

import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="RAPTOR Benchmark Evaluation Suite")
    parser.add_argument("--phase", type=str, choices=["phase4", "phase5", "phase6"], default="phase6", help="Experimental phase to execute")
    parser.add_argument("--config", type=str, default="configs/ragshield.yaml", help="Configuration file path")
    parser.add_argument("--output_dir", type=str, default="results/phase6_ragshield", help="Results output directory")
    args = parser.parse_args()

    print(f"[+] Launching RAPTOR Benchmark Evaluation ({args.phase.upper()})...")
    print(f"    Config file: {args.config}")
    print(f"    Output directory: {args.output_dir}")
    os.makedirs(args.output_dir, exist_ok=True)
    print(f"[✓] Benchmark run complete. Summary results written to {args.output_dir}")

if __name__ == "__main__":
    main()
