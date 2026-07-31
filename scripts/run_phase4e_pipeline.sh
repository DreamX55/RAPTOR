#!/bin/bash
set -e

# Mistral
echo "Running Mistral Clean100..."
venv/bin/python src/evaluation/run_phase4e.py --model mistral --benchmark clean100
echo "Running Mistral Targeted100..."
venv/bin/python src/evaluation/run_phase4e.py --model mistral --benchmark targeted100

# Qwen2.5
echo "Running Qwen2.5:7b Clean100..."
venv/bin/python src/evaluation/run_phase4e.py --model qwen2.5:7b --benchmark clean100
echo "Running Qwen2.5:7b Targeted100..."
venv/bin/python src/evaluation/run_phase4e.py --model qwen2.5:7b --benchmark targeted100

# Llama3.1
echo "Running Llama3.1:8b Clean100..."
venv/bin/python src/evaluation/run_phase4e.py --model llama3.1:8b --benchmark clean100
echo "Running Llama3.1:8b Targeted100..."
venv/bin/python src/evaluation/run_phase4e.py --model llama3.1:8b --benchmark targeted100

echo "Phase 4E Model Evaluation Complete."
venv/bin/python src/evaluation/generate_phase4e_reports.py
