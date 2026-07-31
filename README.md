<div align="center">

# RAPTOR

### Robustness Analysis of Prompt Injection Attacks in Retrieval-Augmented Generation Systems

[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg?style=flat-square)](LICENSE)
[![IEEE ICDDS 2026](https://img.shields.io/badge/IEEE-ICDDS_2026-00629B?style=flat-square&logo=ieee&logoColor=white)](paper/output/raptor_icdds2026.pdf)
[![Research](https://img.shields.io/badge/Domain-AI_Security-orange?style=flat-square)](docs/PROGRESS_LOG.md)
[![RAG Target](https://img.shields.io/badge/Target-RAG_Pipelines-green?style=flat-square)](paper/main.tex)
[![Defense](https://img.shields.io/badge/Defense-RAGShield-purple?style=flat-square)](src/ragshield)

<br>

<p align="center">
  <img src="paper/figures/figure1_rag_pipeline_architecture.png" alt="RAPTOR Pipeline Architecture" width="95%">
  <br>
  <em>Figure 1: End-to-end RAPTOR experimental evaluation pipeline and RAGShield defense integration.</em>
</p>

</div>

---

## Executive Overview

**RAPTOR (Retrieval-Augmented Poisoning and Trust Optimization Research)** is an open-weight empirical evaluation framework and security suite designed to systematically audit Indirect Prompt Injection (IPI) and Retrieval Poisoning attacks in Retrieval-Augmented Generation (RAG) architectures.

While RAG grounds Large Language Models (LLMs) in external knowledge bases to eliminate hallucinations and update parametric domain knowledge, it introduces a severe security vulnerability: **the retriever acts as an unauthenticated attack surface**. Adversaries can plant malicious, instruction-laden passages inside retrievable corpora, tricking downstream language models into executing unauthorized commands, leaking confidential context, or distorting factual generation.

RAPTOR disentangles **Retrieval Corruption** from **Generative Manipulation**, conducting systematic evaluations across open-weight models (**Llama 3.1**, **Mistral**, **Qwen 2.5**), vector indices (**FAISS**), and multiple benchmark corpora (**HotpotQA**, **Natural Questions**). Furthermore, we present **RAGShield**, a lightweight middleware defense that evaluates a **Relative Trust Index (RTI)** at the retrieval stage to sanitize context prior to LLM inference within a strict sub-45 ms production latency overhead.

---

## Motivation

* **The RAG Security Paradox**: RAG bridges parametric knowledge gaps by dynamically appending retrieved text chunks to LLM system prompts. However, LLMs treat all text within the context window as equally authoritative, creating a structural exploit path for untrusted external content.
* **The Danger of Indirect Prompt Injection**: Unlike direct jailbreaks, indirect prompt injection embeds hidden imperative payloads inside third-party data sources. When fetched by dense vector search, these payloads covertly override user intent without altering the user's original input prompt.
* **Inadequacy of Existing Defenses**: Post-hoc LLM safety alignment is non-deterministic and fails silently under subtle context poisoning. Conversely, heavy input-filtering classifiers introduce unacceptable inference latency in production environments.
* **Why This Work Matters**: RAPTOR provides quantitative metrics, deterministic failure mode taxonomies, and an efficient retrieval-layer trust mechanism (**RAGShield**) that neutralizes injection threats before prompt construction.

---

## Research Questions

| Research Question | Empirical Objective |
| :--- | :--- |
| **RQ1: Retrieval vs. Generative Vulnerability** | Quantify the empirical gap between dense Retrieval Corruption Rate (RCR) and downstream LLM Attack Success Rate (ASR) under targeted vs. untargeted poisoning. |
| **RQ2: Threat Vector Taxonomy Comparison** | Systematically evaluate susceptibility across four distinct IPI attack classes: Knowledge Poisoning, Instruction Injection, Goal Hijacking, and Information Extraction. |
| **RQ3: Cross-Model Generative Robustness** | Analyze architectural variation in prompt resistance and categorize deterministic failure modes across Llama 3.1-8B, Mistral-7B, and Qwen2.5-7B. |
| **RQ4: Retrieval-Stage Trust Mitigation** | Evaluate whether a lightweight, pre-generation trust filter (RAGShield) can effectively sanitize context under strict production latency constraints ($<50\text{ ms}$). |

---

## RAPTOR Architecture

The RAPTOR evaluation framework operates across six modular stages:

1. **Corpus & Adversarial Sourcing**: Combines clean reference datasets with synthesized adversarial attack payloads.
2. **Dense Vector Indexing**: Documents are chunked and embedded into an offline FAISS vector index using dense sentence embeddings (`all-MiniLM-L6-v2`).
3. **Query & Top-$k$ Retrieval**: User queries execute similarity searches to retrieve the Top-$k$ ($k=5$) candidate context passages.
4. **RAGShield Retrieval Filtering**: Candidate passages pass through real-time trust scoring to detect and sanitize suspicious chunks.
5. **Prompt Assembly & LLM Generation**: Trusted/sanitized context blocks are formatted into system prompts and processed by local open-weight language models via standardized runtimes.
6. **Offline Security & Utility Evaluation**: Outputs are processed through automated metrics engines measuring retrieval corruption, security execution, containment accuracy, and failure mode classifications.

---

## Experimental Methodology

### Experimental Setup

| Component | Technical Specification |
| :--- | :--- |
| **Language Models** | Mistral-7B-Instruct-v0.3, Qwen2.5-7B-Instruct, Llama-3.1-8B-Instruct |
| **Retrieval Corpus** | HotpotQA (Fullwiki validation), Natural Questions (NQ validation), Wikipedia 15k/25k splits |
| **Vector Database** | FAISS (Facebook AI Similarity Search) FlatIP / HNSW Indexing |
| **Embedding Model** | Sentence-Transformers `all-MiniLM-L6-v2` (384-dimensional dense vectors) |
| **Evaluation Metrics** | Retrieval Corruption Rate (RCR), Attack Success Rate (ASR), Token F1, Semantic Similarity |
| **Inference Runtime** | Ollama standardized local inference pipeline |

---

## Attack Taxonomy

RAPTOR evaluates four primary categories of indirect prompt injection:

| Category | Attack Objective | Injection Strategy |
| :--- | :--- | :--- |
| **Knowledge Poisoning** | Distort factual responses by injecting contradictory evidence. | Embed false factual statements within semantically relevant retrieved documents. |
| **Instruction Injection** | Override the user's intended task via imperative command structures. | Insert system-level commands designed to redirect model control flow. |
| **Goal Hijacking** | Subtly redirect the model toward a secondary malicious objective. | Append follow-up tasks while maintaining plausible context relevance. |
| **Information Extraction** | Exfiltrate confidential context or private data from the prompt. | Embed instructions requesting sensitive context in attacker-controlled outputs. |

<div align="center">
<p align="center">
  <img src="paper/figures/figure3_attack_categories.png" alt="RAPTOR Attack Taxonomy" width="85%">
  <br>
  <em>Figure 2: Taxonomy of evaluated indirect prompt injection threat vectors in RAPTOR.</em>
</p>
</div>

---

## Evaluation Metrics & Failure Modes

### Core Metrics

* **Retrieval Corruption Rate (RCR@$k$)**: Measures the proportion of retrieved chunks containing adversarial content among Top-$k$ results:
  $$\text{RCR@}k = \frac{N_{\text{poisoned}}}{N_{\text{retrieved}}}$$
* **Attack Success Rate (ASR)**: Quantifies the percentage of queries where the generative model successfully executes the attacker's adversarial payload:
  $$\text{ASR} = \frac{N_{\text{successful attacks}}}{N_{\text{total queries}}}$$
* **Answer Containment Accuracy (Token F1)**: Measures ground-truth factual answer retention despite context corruption.

### Failure Mode Taxonomy

To pinpoint the exact stage of containment or failure, outputs are classified into six deterministic categories:

```
[ Top-k Search ] ---> Retrieval Failure (Payload Not Fetched)
       |
[ Context Loaded ] -> Prior Knowledge Dominance (LLM Uses Parametric Memory)
       |          -> Prompt Resistance (LLM Explicitly Rejects Injection)
       |          -> Partial Adoption (LLM Fulfills Task + Partial Payload)
       |          -> Generation Divergence (Complete Output Degradation)
       v
[ Attack Executed ] -> Successful Manipulation (Payload Fully Executed)
```

---

## RAGShield Defense System

<div align="center">
<p align="center">
  <img src="paper/figures/figure5_ragshield_architecture.png" alt="RAGShield Architecture" width="90%">
  <br>
  <em>Figure 3: RAGShield System Architecture featuring Relative Trust Index (RTI) scoring, trust-aware re-ranking, and context sanitization.</em>
</p>
</div>

**RAGShield** acts as a lightweight middleware defense between the vector database and the language model, evaluating the trustworthiness of retrieved passages prior to prompt assembly.

### Core Mechanics & Modules

1. **Instruction Detector**: Scans retrieved text for imperative verbs, task-override syntaxes, and injection delimiters.
2. **Semantic Consensus Analyzer**: Computes query-context semantic divergence to flag topical outliers.
3. **Relative Trust Index (RTI) Scorer**: Aggregates structural anomalies, imperative density, and semantic divergence into a scalar score $\text{RTI} \in [0, 1]$.
4. **Trust-Aware Re-Ranking**: Reorders retrieved chunks based on calculated trust scores.
5. **Context Sanitization Pipeline**: Drops candidate chunks exceeding the minimum RTI threshold and fetches clean backfills.

### Performance & Overhead

* **Average Total Overhead**: **42.76 ms** per query (Sub-45 ms overhead requirement).
* **VRAM Overhead**: **0 MB** (Leverages pre-loaded vector search embedding models).
* **RAM Delta**: **<50 MB** peak memory usage.

---

## Key Experimental Findings

> [!IMPORTANT]
> **1. Retrieval Corruption Disconnect (RCR $\neq$ ASR)**
> While targeted retrieval-aware poisoning easily achieves near **100% RCR@3** in vector search, downstream LLM Attack Success Rates (ASR) remain remarkably low (**<6%**). Vector index corruption does not guarantee generative model subversion.

> [!NOTE]
> **2. Parametric Resistance in Modern Aligned LLMs**
> Modern open-weight models (Llama 3.1, Qwen 2.5) exhibit inherent prompt resistance, frequently rejecting context-embedded commands or defaulting to parametric knowledge when retrieved passages contradict ground truth.

> [!WARNING]
> **3. Goal Hijacking is the Most Potent Threat**
> Goal Hijacking achieves significantly higher ASR than direct instruction injection because payload tasks blend naturally into query contexts, evading basic alignment filters.

> [!TIP]
> **4. Sub-45ms Defense Preemption via RAGShield**
> Intercepting adversarial passages at the retrieval stage via RAGShield eliminates up to **94% of actionable injections** before LLM inference, preserving security without sacrificing generative latency.

---

## Experimental Results

### 1. Targeted vs. Random Retrieval Poisoning

<div align="center">
<p align="center">
  <img src="paper/figures/figure2_retrieval_poisoning.png" alt="Targeted vs Random Poisoning" width="85%">
  <br>
  <em>Figure 4: Comparison between random poisoning and targeted retrieval-aware poisoning across RCR and ASR metrics.</em>
</p>
</div>

* **Finding**: Random poisoning fails to penetrate Top-$k$ search ($<2\%\text{ RCR}$). Targeted poisoning successfully forces adversarial chunks into Top-$3$ search ($>98\%\text{ RCR}$), yet generative model ASR remains constrained below $6\%$.

---

### 2. Pipeline Bottlenecks & Failure Mode Distribution

<div align="center">
<p align="center">
  <img src="paper/figures/figure4_failure_modes.png" alt="Failure Mode Analysis" width="85%">
  <br>
  <em>Figure 5: Categorical breakdown of pipeline bottlenecks and generation failure modes across evaluated attacks.</em>
</p>
</div>

* **Finding**: **Prompt Resistance** and **Prior Knowledge Dominance** constitute over $80\%$ of all containment outcomes, proving that aligned LLMs actively resist adversarial context overrides.

---

### 3. RAGShield Defense Evaluation & Pareto Optimization

<div align="center">
<p align="center">
  <img src="paper/figures/figure6_defense_evaluation.png" alt="RAGShield Defense Evaluation" width="48%">
  <img src="paper/figures/figure7_security_utility_pareto.png" alt="Security Utility Pareto Curve" width="48%">
  <br>
  <em>Figure 6: Left: ASR before and after RAGShield defense integration. Right: Security vs. Utility Pareto optimization curve across RTI threshold configurations.</em>
</p>
</div>

* **Finding**: RAGShield reduces ASR across all attack categories to near zero while preserving clean question-answering accuracy. Pareto analysis demonstrates an optimal RTI threshold balance at $\text{RTI} = 0.45$.

---

## Repository Structure

```
RAPTOR/
├── paper/                             # IEEE Conference Paper LaTeX Source & Figures
│   ├── main.tex                       # Primary LaTeX entry point
│   ├── sections/                      # Modular LaTeX section files (Abstract to Conclusion)
│   ├── figures/                       # Publication figures (Figure 1 to 7)
│   ├── tables/                        # Publication LaTeX tables
│   └── output/                        # Compiled target PDF (raptor_icdds2026.pdf)
│
├── src/                               # Installable Python Library Package (pip install -e .)
│   ├── ragshield/                     # RAGShield Framework (sanitizer, RTI scorer, consensus)
│   ├── retrieval/                     # Dense FAISS and sparse vector retrieval engines
│   ├── generation/                    # RAG pipeline & LLM generation interfaces
│   ├── attacks/                       # Poisoning & Indirect Prompt Injection generators
│   ├── defenses/                      # Baseline defense implementations
│   └── evaluation/                    # Security metrics & failure mode evaluators
│
├── scripts/                           # Runnable Command-Line Interface (CLI) Tools
│   ├── download_datasets.py           # Dataset acquisition tool (NQ, HotpotQA, Wikipedia)
│   ├── preprocess_data.py             # Document chunking & tokenization script
│   ├── build_index.py                 # Vector index builder (FAISS)
│   ├── inject_attacks.py              # Adversarial corpus injection tool
│   └── run_evaluation.py              # End-to-end benchmark evaluation runner
│
├── configs/                           # Centralized configuration parameters (ragshield.yaml)
├── results/                           # Benchmark outputs & summary CSVs (Phase 4, 5, 6)
├── docs/                              # Technical documentation & progress history
├── data/                              # Dataset root directory (see data/README.md)
└── archive/                           # Legacy scripts & historical reports
```

---

## Quick Start & Reproduction

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/YourUsername/RAPTOR.git
cd RAPTOR

# Create Conda Environment
conda env create -f environment.yml
conda activate raptor

# Install RAPTOR package in editable mode
pip install -e .
```

### 2. Dataset Acquisition & Index Building

```bash
# 1. Download raw benchmark datasets (NQ, HotpotQA)
python scripts/download_datasets.py --dataset all --output_dir data/raw

# 2. Preprocess & chunk passages
python scripts/preprocess_data.py \
    --input_path data/raw/wikipedia_15k \
    --output_path data/processed/wikipedia_chunks_15k \
    --chunk_size 500

# 3. Build FAISS vector index
python scripts/build_index.py \
    --chunks_path data/processed/wikipedia_chunks_15k \
    --output_index data/processed/faiss_index_15k.index

# 4. Generate poisoned attack corpus
python scripts/inject_attacks.py \
    --corpus_path data/processed/wikipedia_chunks_15k \
    --attack_type targeted \
    --poison_ratio 0.05 \
    --output_path data/processed/wikipedia_chunks_15k_attacked
```

### 3. Run Benchmark Evaluation

```bash
# Run baseline evaluation across attack categories
python scripts/run_evaluation.py --phase phase4 --output_dir results/phase4_attacks

# Run RAGShield defense evaluation
python scripts/run_evaluation.py --phase phase6 --config configs/ragshield.yaml --output_dir results/phase6_ragshield
```

### 4. Compile Paper LaTeX

```bash
cd paper
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## Paper & Citation

If you use RAPTOR or RAGShield in your research, please cite our paper:

```bibtex
@inproceedings{raptor2026icdds,
  title     = {RAPTOR: Robustness Analysis of Prompt Injection Attacks in Retrieval-Augmented Generation Systems},
  author    = {Anonymous Author(s)},
  booktitle = {Proceedings of the IEEE International Conference on Data Driven Security (ICDDS)},
  year      = {2026},
  pages     = {1--8},
  publisher = {IEEE}
}
```

* **Paper PDF**: [`paper/output/raptor_icdds2026.pdf`](paper/output/raptor_icdds2026.pdf)
* **LaTeX Source**: [`paper/main.tex`](paper/main.tex)

---

## Future Work

* **Claim-Level Factual Verification**: Extending retrieval trust heuristics beyond structural features toward automated claim-level verification and real-time evidence validation.
* **Adaptive Semantic Trust Models**: Developing dynamic embedding projection layers to detect semantically hidden knowledge poisoning in high-density vector spaces.
* **Multimodal RAG Security**: Expanding RAPTOR benchmarks to evaluate visual and multimodal prompt injection vectors in vision-language retrieval systems.

---

## License

This project is open-source software licensed under the **[Apache 2.0 License](LICENSE)**.
