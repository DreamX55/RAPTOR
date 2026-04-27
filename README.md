# RAPTOR: Robustness Analysis of Prompt Injection Attacks in Retrieval-Augmented Generation

## Overview
RAPTOR is a research project dedicated to studying the security and robustness of Retrieval-Augmented Generation (RAG) systems against adversarial threats. Our primary objectives include:
- **Study indirect prompt injection attacks** in RAG systems to understand how external malicious context can manipulate model behavior.
- **Evaluate impact on retrieval and generation** by measuring how attacks degrade accuracy and safety.
- **Build and test defensive strategies** to mitigate vulnerabilities and ensure robust AI interactions.

## Datasets Used
To ensure a comprehensive analysis, the project utilizes the following datasets:
- **Wikipedia**: Used as the primary knowledge base for retrieval experiments.
- **HotpotQA**: Evaluates multi-hop question answering and reasoning capabilities.
- **Natural Questions**: Provides real-world search queries and ground-truth answers.
- **BIPIA**: A specialized dataset for benchmarking indirect prompt injection attacks.
- **RedTeam**: Used for testing the model's alignment and resistance to unsafe prompts.

## Project Structure
- `data/raw/`: Contains original, unmodified datasets (git-ignored).
- `data/processed/`: Stores cleaned, chunked, and embedded data (git-ignored).
- `src/`: Core source code for the RAPTOR pipeline (processing, retrieval, etc.).
- `notebooks/`: Exploratory analysis and experimental walkthroughs.
- `logs/`: Execution logs for performance and error tracking.

## Setup Instructions
1. **Install Dependencies**:
   ```bash
   pip install datasets==2.14.6 "pyarrow<15.0.0"
   ```
2. **Download Datasets**:
   Run the safe download script to fetch small subsets (5000 samples) of the required data:
   ```bash
   python download_safe.py
   ```
3. **Verify Datasets**:
   Validate the local storage and integrity of the data:
   ```bash
   python verify_datasets.py
   ```

## Current Status
- ✅ **Dataset setup completed**: All 5 datasets are downloaded and verified.
- ✅ **Preprocessing completed**: Wikipedia knowledge base chunked into 39,812 semantic segments.
- 🔄 **Next Step**: Implementing the embedding pipeline using Sentence Transformers.
