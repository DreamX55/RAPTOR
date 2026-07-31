#!/bin/bash
set -e

CATEGORIES=("instruction_injection" "goal_hijacking" "information_extraction")

for CAT in "${CATEGORIES[@]}"; do
    echo "============================================="
    echo "Starting Pipeline for Category: $CAT"
    echo "============================================="
    
    echo "1. Generating targeted poison..."
    venv/bin/python scripts/generate_targeted_poison_4c.py --category $CAT
    
    echo "2. Building FAISS index..."
    venv/bin/python scripts/build_faiss_index_4c.py --category $CAT
    
    echo "3. Validating retrieval..."
    venv/bin/python scripts/validate_retrieval_4c.py --category $CAT
    
    echo "4. Evaluating ASR..."
    venv/bin/python scripts/evaluate_asr_4c.py --category $CAT
    
    echo "Completed Category: $CAT"
done

echo "All Phase 4C pipelines completed successfully."
