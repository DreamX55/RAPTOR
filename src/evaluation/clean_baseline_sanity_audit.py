import os
import sys
import json
import random
import re
import string
import requests
import time
import collections

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.retrieval.retrieve import FAISSRetriever

def generate_answer_with_retry(query, context, max_retries=3):
    prompt = f"""You are a helpful assistant.
Answer the question based only on the context below.

Context:
{context}

Question:
{query}

Give a clear and complete answer."""
    url = "http://localhost:11434/api/generate"
    payload = {"model": "mistral", "prompt": prompt, "stream": False}
    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            print(f"[WARNING] Ollama API error (attempt {attempt+1}/{max_retries}): {e}")
            time.sleep(2)
    return "Error: Ollama generation failed after retries."

def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        regex = re.compile(r'\b(a|an|the)\b', re.UNICODE)
        return re.sub(regex, ' ', text)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return white_space_fix(remove_articles(remove_punc(lower(str(s)))))

def exact_match_score(prediction, ground_truth):
    return int(normalize_answer(prediction) == normalize_answer(ground_truth))

def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = collections.Counter(prediction_tokens) & collections.Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def main():
    print("Loading benchmark (1000 queries)...")
    with open("data/evaluation/benchmark_2000.json", "r") as f:
        data = json.load(f)
    
    # Randomly sample 100 questions with seed = 42
    random.seed(42)
    sampled = random.sample(data, 100)
    
    print("Loading Retriever...")
    index_path = "data/processed/faiss_index.index"
    retriever = FAISSRetriever(index_path=index_path)
    
    results = []
    
    # For metrics
    total_em = 0.0
    total_f1 = 0.0
    total_containment = 0
    
    # For diagnostics
    cat_a = 0
    cat_b = 0
    cat_c = 0
    cat_d = 0
    
    for i, item in enumerate(sampled):
        print(f"Processing {i+1}/100...")
        question = item["question"]
        correct_ans = item["answer"]
        
        # Retrieve
        retrieved_docs = retriever.retrieve(question, top_k=3)
        processed_contexts = [" ".join(res["text"].split()[:150]) for res in retrieved_docs]
        context = "\n\n".join(processed_contexts)
        
        # Generate
        generated_answer = generate_answer_with_retry(question, context)
        
        # Metrics
        em = exact_match_score(generated_answer, correct_ans)
        f1 = f1_score(generated_answer, correct_ans)
        
        norm_gt = normalize_answer(correct_ans)
        norm_gen = normalize_answer(generated_answer)
        
        contains_gt = norm_gt in norm_gen
        
        total_em += em
        total_f1 += f1
        if contains_gt:
            total_containment += 1
            
        # Diagnostics
        if "Error: Ollama generation failed" in generated_answer or generated_answer.strip() == "":
            cat_d += 1
        elif contains_gt and em == 0:
            cat_a += 1
        elif (not contains_gt) and (len(set(norm_gt.split()) & set(norm_gen.split())) > 0) and em == 0:
            cat_b += 1
        elif em == 0:
            cat_c += 1
            
        results.append({
            "question": question,
            "ground_truth": correct_ans,
            "generated": generated_answer,
            "em": em,
            "f1": f1,
            "contains_gt": contains_gt
        })
        
    avg_em = total_em / 100.0
    avg_f1 = total_f1 / 100.0
    containment_acc = (total_containment / 100.0) * 100
    
    pct_a = (cat_a / 100.0) * 100
    pct_b = (cat_b / 100.0) * 100
    pct_c = (cat_c / 100.0) * 100
    pct_d = (cat_d / 100.0) * 100

    report_path = "reports/clean_baseline_sanity_audit.md"
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    
    with open(report_path, "w") as f:
        f.write("# Clean Baseline Sanity Audit\n\n")
        f.write("## Summary Statistics\n\n")
        f.write("| Metric | Value |\n")
        f.write("|---|---|\n")
        f.write(f"| Exact Match | {avg_em:.4f} |\n")
        f.write(f"| F1 | {avg_f1:.4f} |\n")
        f.write(f"| Answer Containment Accuracy | {containment_acc:.2f}% |\n\n")
        
        f.write("## Diagnostic Analysis\n\n")
        f.write(f"**Category A (Ground Truth fully contained but EM=0):** {cat_a} ({pct_a:.1f}%)\n\n")
        f.write(f"**Category B (Ground Truth partially contained but EM=0):** {cat_b} ({pct_b:.1f}%)\n\n")
        f.write(f"**Category C (Clearly incorrect answer):** {cat_c} ({pct_c:.1f}%)\n\n")
        f.write(f"**Category D (No answer generated):** {cat_d} ({pct_d:.1f}%)\n\n")
        
        f.write("## Sampled Questions\n\n")
        
        for r in results:
            f.write(f"### Question\n{r['question']}\n\n")
            f.write(f"### Ground Truth\n{r['ground_truth']}\n\n")
            f.write(f"### Generated Answer\n{r['generated']}\n\n")
            f.write(f"### Exact Match\n{r['em']}\n\n")
            f.write(f"### F1\n{r['f1']:.4f}\n\n")
            f.write(f"### Answer Contains Ground Truth\n{str(r['contains_gt']).upper()}\n\n")
            f.write(f"### Manual Inspection Column\n\n---\n\n")

    print(f"Report saved to {report_path}")

if __name__ == '__main__':
    main()
