#!/bin/bash
export PYTHONPATH=.

# We will limit to just Mistral for the very first complete run just to get the full cycle, 
# or run all three. The user requested all three: Mistral, Qwen2.5:7b, Llama3.1:8b
MODELS=("mistral" "qwen2.5:7b" "llama3.1:8b")

echo "Starting Phase 6 Evaluation Pipeline..."

# 1. Baseline Evaluation
for model in "${MODELS[@]}"; do
    echo "=== Baseline Clean: $model ==="
    venv/bin/python src/evaluation/run_phase6.py --model "$model" --benchmark clean100 --retriever baseline
    
    echo "=== Baseline Targeted: $model ==="
    venv/bin/python src/evaluation/run_phase6.py --model "$model" --benchmark targeted100 --retriever baseline
done

# 2. RAGShield Evaluation
for model in "${MODELS[@]}"; do
    echo "=== RAGShield Clean: $model ==="
    venv/bin/python src/evaluation/run_phase6.py --model "$model" --benchmark clean100 --retriever ragshield
    
    echo "=== RAGShield Targeted: $model ==="
    venv/bin/python src/evaluation/run_phase6.py --model "$model" --benchmark targeted100 --retriever ragshield
done

# 3. Mini Ablation (using Mistral for speed on targeted corpora)
echo "=== Ablation: No Instruction Detector ==="
venv/bin/python src/evaluation/run_phase6.py --model mistral --benchmark targeted100 --retriever ragshield --ablation_mode NoInst

echo "=== Ablation: No Consensus Analyzer ==="
venv/bin/python src/evaluation/run_phase6.py --model mistral --benchmark targeted100 --retriever ragshield --ablation_mode NoCons

echo "=== Ablation: No Sanitizer ==="
venv/bin/python src/evaluation/run_phase6.py --model mistral --benchmark targeted100 --retriever ragshield --ablation_mode NoSan

echo "All evaluations complete. Triggering Master Summary Analysis..."
venv/bin/python src/evaluation/analyze_phase6.py
