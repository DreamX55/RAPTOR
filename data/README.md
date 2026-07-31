# RAPTOR Data Directory Setup & Instructions

This directory manages all raw and processed dataset assets for the RAPTOR project.

To keep the git repository lightweight and fast to clone, **binary dataset files (`.arrow`, `.index`, `.parquet`) are excluded from git tracking**.

---

## Directory Structure

```
data/
├── README.md             # This instruction guide
├── raw/                  # Downloaded raw datasets (NQ, HotpotQA, BIPIA, Wikipedia)
└── processed/            # Chunked passages, FAISS vector indexes, and attack corpora
```

---

## Dataset Acquisition & Setup

To fetch and preprocess the required datasets for reproducing RAPTOR experiments, run the following unified CLI commands from the project root:

### 1. Download Raw Datasets
```bash
python scripts/download_datasets.py --dataset all --output_dir data/raw
```

### 2. Preprocess & Chunk Passages
```bash
python scripts/preprocess_data.py \
    --input_path data/raw/wikipedia_15k \
    --output_path data/processed/wikipedia_chunks_15k \
    --chunk_size 500 \
    --chunk_overlap 50
```

### 3. Build Vector Indexes (FAISS)
```bash
python scripts/build_index.py \
    --chunks_path data/processed/wikipedia_chunks_15k \
    --output_index data/processed/faiss_index_15k.index
```

### 4. Inject Benchmark Attacks
```bash
python scripts/inject_attacks.py \
    --corpus_path data/processed/wikipedia_chunks_15k \
    --attack_type targeted \
    --poison_ratio 0.05 \
    --output_path data/processed/wikipedia_chunks_15k_attacked_5pct
```
