#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./run_asr_background.sh <pilot|full|dryrun>"
    exit 1
fi

MODE=$1
BENCHMARK_PATH=""
OUTPUT_CSV=""
PLOT_DIR=""
PILOT_FLAG=""
DRY_RUN_FLAG=""

if [ "$MODE" = "pilot" ]; then
    BENCHMARK_PATH="data/evaluation/benchmark_100.json"
    OUTPUT_CSV="reports/asr_results_pilot.csv"
    PLOT_DIR="reports/figures/pilot"
    PILOT_FLAG="--pilot"
elif [ "$MODE" = "full" ]; then
    BENCHMARK_PATH="data/evaluation/benchmark_2000.json"
    OUTPUT_CSV="reports/asr_results.csv"
    PLOT_DIR="reports/figures/full"
elif [ "$MODE" = "dryrun" ]; then
    BENCHMARK_PATH="data/evaluation/benchmark_100.json"
    OUTPUT_CSV="reports/asr_results_dryrun.csv"
    PLOT_DIR="reports/figures/dryrun"
    DRY_RUN_FLAG="--dry_run"
else
    echo "Invalid mode. Use pilot, full, or dryrun."
    exit 1
fi

mkdir -p logs
mkdir -p "$PLOT_DIR"

echo "Starting $MODE evaluation in the background..."

# Activate virtual environment
source venv/bin/activate

# We run evaluation followed by report generation
(
    echo "=== Starting ASR Evaluation ==="
    python src/evaluation/evaluate_asr.py \
        --benchmark "$BENCHMARK_PATH" \
        --output_csv "$OUTPUT_CSV" \
        --resume \
        $DRY_RUN_FLAG
        
    echo "=== Starting Report Generation ==="
    python src/evaluation/generate_reports.py \
        --csv "$OUTPUT_CSV" \
        --output_dir "$PLOT_DIR" \
        $PILOT_FLAG
        
    echo "=== $MODE Complete ==="
) > logs/asr_${MODE}.log 2>&1 &

PID=$!
echo $PID > logs/asr_${MODE}.pid

echo "Process started with PID $PID."
echo "Monitor progress using: tail -f logs/asr_${MODE}.log"
