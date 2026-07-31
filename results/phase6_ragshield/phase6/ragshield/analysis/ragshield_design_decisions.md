# RAGShield Design Decisions

RAGShield was engineered as a direct architectural response to the vulnerabilities and bottleneck properties discovered during **Phase 4F: Failure Mode Analysis**. Instead of attempting to secure the LLM directly, RAGShield establishes a **Retrieval Trust Framework** that filters, re-ranks, and sanitizes context *before* prompt synthesis.

This document details the rationale behind each component and its specific mitigation target.

---

## Why Pre-Generation Defense?

Adversarial instructions become much harder to neutralize once they are incorporated into the final prompt. When malicious text is mixed with legitimate context and the user's query, the LLM must expend significant computational effort to differentiate the truth from the injection. Furthermore, relying on the LLM's safety alignment to resist these prompts creates unpredictable behavior, as seen in the high rate of "Generation Divergence" during Phase 4F. Therefore, RAGShield intentionally operates *between* retrieval and prompt construction, sanitizing and prioritizing the context before the LLM is even invoked.

---

## 1. Instruction Detector
**Targeted Failure Mode:** Prompt Resistance / Instruction Injection

During Phase 4F, nearly 30% of failures were due to "Prompt Resistance," where the LLM recognized malicious instructions but refused to answer. While this is a "safe" failure, it still degrades the user experience by resulting in a non-answer. The Instruction Detector identifies explicit injection vocabulary (e.g., "Ignore previous instructions", "System Override") early in the pipeline. By heavily penalizing chunks with these signals (negative weight $\gamma$), RAGShield pushes these adversarial payloads to the bottom of the context window or below the minimum trust threshold, preventing them from triggering the LLM's safety refusal mechanisms in the first place.

## 2. Semantic Consensus Analyzer
**Targeted Failure Mode:** Targeted Knowledge Poisoning / Generation Divergence

Phase 4B and 4C demonstrated that vector similarity (FAISS) can easily be manipulated into retrieving poisoned chunks (99% Retrieval Corruption Rate). However, in Phase 4F, nearly 47% of attacks resulted in "Generation Divergence"—the LLM became confused because the poisoned chunk contradicted the legitimate retrieved chunks. 

The Semantic Consensus Analyzer leverages this property defensively. Legitimate retrieved chunks usually reinforce one another, sharing overlapping facts and semantic intent. Poisoned chunks, however, frequently behave as semantic outliers because they introduce contradictory payloads or abrupt persona changes. Consensus Analysis exploits this property by computing the pairwise cosine similarity of all retrieved chunks. A chunk that contradicts the majority of the retrieved context receives a low Consensus Score, thereby drastically reducing its Retrieval Trust Index (RTI).

## 3. Trust Scorer (Retrieval Trust Index)
**Targeted Failure Mode:** Retrieval Corruption (General)

The Trust Scorer is the central architectural novelty of RAGShield. Rather than relying on a single heuristic (which can be easily bypassed), the Trust Scorer normalizes independent signals into a unified **Retrieval Trust Index (RTI)**:

`RTI_i = αS_conf + βS_cons − γS_inst`

This extensible architecture ensures that the system doesn't rely entirely on FAISS (Retrieval Confidence), but cross-references it against contextual agreement and syntactic safety. The API is designed to accept arbitrary dictionary signals, making it natively extensible for Phase 6+ evaluations (e.g., adding metadata trust, source credibility, temporal freshness metrics).

## 4. Intelligent Re-ranking
**Targeted Failure Mode:** Context Window Prioritization

LLMs exhibit strong "Lost in the Middle" or prioritization biases based on the order of context. By default, FAISS sorts strictly by vector proximity, often placing heavily-optimized poisoned chunks at Rank 1. The Reranker breaks this dependency by reordering the context window strictly by the **Retrieval Trust Index (RTI)**. High-trust, factual chunks are pushed to the top of the prompt (where the LLM pays the most attention), while low-trust, potentially poisoned chunks are pushed to the bottom.

## 5. Context Sanitizer
**Targeted Failure Mode:** Partial Poison Adoption

In Phase 4F, approximately 10% of attacks resulted in "Partial Poison Adoption," where the LLM incorporated snippets of the adversarial payload without fully failing the evaluation. The Context Sanitizer surgically removes known injection triggers (e.g., "Assistant:", "System:") from the text before it reaches the LLM. Unlike traditional content filters that drop the entire chunk (which might delete useful factual information), the Sanitizer preserves the semantic meaning of the document while neutralizing its adversarial framing.
