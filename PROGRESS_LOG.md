# PROGRESS LOG: RAPTOR Research Project

## Project Overview
- **Project Title**: RAPTOR (Robustness Analysis of Prompt Injection Attacks in Retrieval-Augmented Generation)
- **Objective**: To systematically analyze and mitigate the risks posed by indirect prompt injection attacks within RAG architectures.
- **Core Idea**: Developing a resilient RAG pipeline by evaluating attack surfaces across retrieval and generation phases and implementing robust defensive filters.

---

## Dataset Setup Phase

| Dataset | Source | Justification |
|---------|--------|---------------|
| **Wikipedia** | `wikimedia/wikipedia` | Provides a diverse, factual knowledge base for standard retrieval. |
| **HotpotQA** | `hotpot_qa` | Evaluates the system's ability to handle multi-hop reasoning and complex queries. |
| **Natural Questions** | `natural_questions` | Benchmarks against real-world Google search queries and short answers. |
| **BIPIA** | `microsoft/BIPIA` | A specialized benchmark for Indirect Prompt Injection Attacks (IPIA). |
| **RedTeam** | `Anthropic/hh-rlhf` | Tests model safety, alignment, and resistance to adversarial jailbreaking. |

---

## System Architecture Plan
The RAPTOR system follows a modular RAG architecture:
1. **Knowledge Base**: Curated subsets (5,000 samples each) of the primary datasets.
2. **Preprocessing**: Document chunking and metadata enrichment.
3. **Embeddings**: Vectorization using state-of-the-art sentence transformers.
4. **Retriever**: High-performance similarity search using FAISS.
5. **Generation**: LLM-based response synthesis with integrated safety gates.
6. **Evaluation**: Metrics for both retrieval accuracy and adversarial robustness.

---

## Progress Log

### Phase 1: Initialization & Data Acquisition

#### 2026-04-26 | Project Initialization
- **Task**: Initialize project directory structure.
- **Tool**: Antigravity (Conversation f7f70ba6)
- **Changes**: Created `data/`, `src/`, `notebooks/`, and `logs/` folders.
- **Reason**: Establish a clean, modular structure for research reproducibility.
- **Outcome**: Base environment ready.

#### 2026-04-27 | Safe Download Pipeline
- **Task**: Create a memory-efficient dataset download script.
- **Tool**: Antigravity
- **Prompt**: "Set up a safe dataset download pipeline for a RAG project."
- **Changes**: Created `download_safe.py` using HuggingFace `streaming=True`.
- **Reason**: Avoid massive local storage usage (keep total < 1GB) while securing necessary data.
- **Outcome**: Successful subsetting (2,000 samples) of primary datasets.

#### 2026-04-27 | Scaling Data & loader Fixes
- **Task**: Increase dataset size and fix broken loaders.
- **Tool**: Antigravity
- **Changes**: 
    - Updated `LIMIT` from 2,000 to 5,000.
    - Switched Wikipedia loader to `wikimedia/wikipedia` (20231101.en).
    - Replaced BIPIA automation with manual `git clone` instructions.
- **Reason**: 5,000 samples provide better statistical significance; old Wikipedia loader was unstable.
- **Outcome**: All 5 datasets verified and stored in `data/raw/`.

#### 2026-04-27 | Validation & Version Control
- **Task**: Create verification script and initialize Git.
- **Tool**: Antigravity / Manual
- **Changes**:
    - Created `verify_datasets.py` for automated integrity checks.
    - Created `README.md` and `.gitignore`.
    - Initialized Git and pushed to GitHub (`DreamX55/RAPTOR`).
- **Reason**: Ensure data integrity before moving to processing; prepare for collaborative development.
- **Outcome**: Project status is "Clean" and synced with remote.

#### 2026-04-27 | Research Documentation & Logging
- **Task**: Implement systematic research tracking.
- **Tool**: Antigravity
- **Prompt**: "Create a structured research progress documentation file called PROGRESS_LOG.md for the RAPTOR project."
- **Changes**: Created `PROGRESS_LOG.md`.
- **Reason**: To maintain a professional audit trail of all technical decisions and project milestones, facilitating future research paper writing and reproducibility.
- **Outcome**: Comprehensive project log established and integrated into the repository.

#### 2026-04-27 | Data Preprocessing & Chunking
- **Task**: Implement semantic chunking for the Wikipedia knowledge base.
- **Tool**: Antigravity / Python Script
- **Prompt**: "Create a Python script called chunk_wikipedia.py to preprocess and chunk the Wikipedia dataset for a RAG pipeline."
- **Changes**: 
    - Created `chunk_wikipedia.py`.
    - Processed 5,000 raw documents into 39,812 semantic chunks.
    - Saved output to `data/processed/wikipedia_chunks`.
- **Reason**: RAG systems require small, focused context windows (200-300 words) for efficient retrieval and to stay within LLM context limits.
- **Outcome**: Processed knowledge base ready for embedding phase.

#### 2026-04-27 | Structural Refactoring & Modularization
- **Task**: Refactor project structure to organize scripts into a modular `src/` directory.
- **Tool**: Antigravity / Terminal
- **Prompt**: "Refactor the RAPTOR project structure to organize all Python scripts into the src/ directory."
- **Changes**: 
    - Moved core scripts (`download_safe.py`, `chunk_wikipedia.py`, `verify_datasets.py`, etc.) to `src/data_processing/`.
    - Created `__init__.py` files in all functional subdirectories of `src/`.
    - Initialized placeholders for `embedding/`, `retrieval/`, `generation/`, `attacks/`, `defenses/`, and `evaluation/`.
- **Reason**: To enhance codebase maintainability and enable professional modular imports as the RAG pipeline complexity increases.
- **Outcome**: Established a scalable, industry-standard research project architecture.

---

## Decisions & Justifications

### 1. Data Subsetting (5,000 samples)
- **Decision**: Limit datasets to 5,000 samples instead of full corpora.
- **Tradeoff**: Reduces total data variety but allows for rapid iteration and stays within 1GB storage limit. It is sufficient for a "Robustness Analysis" proof-of-concept.

### 2. Semantic Chunking Strategy
- **Decision**: Use sentence-boundary aware chunking with a 200-300 word target.
- **Justification**: Prevents cutting mid-sentence, which preserves local semantic meaning and improves retrieval accuracy. 300 words is a balanced size for most modern LLM context windows (e.g., GPT-3.5/4).

### 3. FAISS vs Managed Vector DB
- **Decision**: Planned use of **FAISS** for local indexing.
- **Justification**: FAISS is lightweight, supports rapid local testing, and doesn't require external cloud API management, making it ideal for research-focused benchmarking.

### 3. Streaming Mode for Downloads
- **Decision**: Enforced `streaming=True` in HuggingFace loaders.
- **Justification**: Crucial for Wikipedia and NQ which are tens of gigabytes in size. Fetches only the required rows without saturating network/disk.

---

## Future Work
- **Embedding Pipeline**: Benchmarking `all-MiniLM-L6-v2` vs `bge-small-en-v1.5` for chunk vectorization.
- **Vector Database**: Implementing local FAISS index for high-speed similarity search.
- **Attack Simulation**: Injecting BIPIA malicious prompts into retrieved context windows.
- **Defense Implementation**: Developing detection-based classifiers and robust prompt templates.
