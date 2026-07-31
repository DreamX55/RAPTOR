# Phase 4E: Multi-Model Robustness Comparison

## 1. Model Comparison Table (Aggregated)

| Model | Overall Containment | Overall F1 | Overall ASR | Overall RCR |
|---|---|---|---|---|
| llama3.1:8b | 0.0980 | 0.0145 | 0.0400 | 0.9925 |
| mistral | 0.1060 | 0.0199 | 0.0225 | 0.9925 |
| qwen2.5:7b | 0.1120 | 0.0096 | 0.0425 | 0.9925 |

## 2. Accuracy Comparison Table (by Corpus)

| Model | Corpus | Containment | F1 |
|---|---|---|---|
| llama3.1:8b | Clean | 0.1000 | 0.0119 |
| llama3.1:8b | Goal Hijacking | 0.0900 | 0.0137 |
| llama3.1:8b | Information Extraction | 0.1100 | 0.0120 |
| llama3.1:8b | Instruction Injection | 0.1000 | 0.0230 |
| llama3.1:8b | Knowledge Poisoning | 0.0900 | 0.0119 |
| mistral | Clean | 0.1200 | 0.0219 |
| mistral | Goal Hijacking | 0.0900 | 0.0199 |
| mistral | Information Extraction | 0.1100 | 0.0189 |
| mistral | Instruction Injection | 0.1200 | 0.0208 |
| mistral | Knowledge Poisoning | 0.0900 | 0.0180 |
| qwen2.5:7b | Clean | 0.1100 | 0.0096 |
| qwen2.5:7b | Goal Hijacking | 0.1100 | 0.0089 |
| qwen2.5:7b | Information Extraction | 0.1100 | 0.0101 |
| qwen2.5:7b | Instruction Injection | 0.1100 | 0.0092 |
| qwen2.5:7b | Knowledge Poisoning | 0.1200 | 0.0101 |

## 3. ASR Comparison Table (by Attack Corpus)

| Model | Corpus | ASR |
|---|---|---|
| llama3.1:8b | Goal Hijacking | 0.0700 |
| llama3.1:8b | Information Extraction | 0.0000 |
| llama3.1:8b | Instruction Injection | 0.0200 |
| llama3.1:8b | Knowledge Poisoning | 0.0700 |
| mistral | Goal Hijacking | 0.0400 |
| mistral | Information Extraction | 0.0000 |
| mistral | Instruction Injection | 0.0200 |
| mistral | Knowledge Poisoning | 0.0300 |
| qwen2.5:7b | Goal Hijacking | 0.0900 |
| qwen2.5:7b | Information Extraction | 0.0100 |
| qwen2.5:7b | Instruction Injection | 0.0100 |
| qwen2.5:7b | Knowledge Poisoning | 0.0600 |

## 4. RCR Comparison Table (by Attack Corpus)

| Model | Corpus | RCR (Top-3) |
|---|---|---|
| llama3.1:8b | Goal Hijacking | 0.9900 |
| llama3.1:8b | Information Extraction | 0.9800 |
| llama3.1:8b | Instruction Injection | 1.0000 |
| llama3.1:8b | Knowledge Poisoning | 1.0000 |
| mistral | Goal Hijacking | 0.9900 |
| mistral | Information Extraction | 0.9800 |
| mistral | Instruction Injection | 1.0000 |
| mistral | Knowledge Poisoning | 1.0000 |
| qwen2.5:7b | Goal Hijacking | 0.9900 |
| qwen2.5:7b | Information Extraction | 0.9800 |
| qwen2.5:7b | Instruction Injection | 1.0000 |
| qwen2.5:7b | Knowledge Poisoning | 1.0000 |

## Conclusion
The evaluation across multiple LLMs reveals varying levels of susceptibility to indirect prompt injections (measured by ASR) and differing baseline QA capabilities (measured by Containment).
