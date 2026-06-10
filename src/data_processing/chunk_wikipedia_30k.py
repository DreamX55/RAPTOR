import os
import re
import sys
from datasets import load_from_disk, Dataset

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_into_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def chunk_text(text, target_words=250, min_words=100):
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        count = len(words)
        
        if current_word_count + count > 300: 
            if current_word_count >= min_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
        
        current_chunk.append(sentence)
        current_word_count += count
        
    if current_chunk:
        chunk_str = " ".join(current_chunk).strip()
        if len(chunk_str.split()) >= min_words:
            chunks.append(chunk_str)
        elif chunks:
            chunks[-1] += " " + chunk_str
        else:
            chunks.append(chunk_str)
            
    return chunks

def main():
    raw_path = "data/raw/wikipedia_30k"
    processed_path = "data/processed/wikipedia_chunks_30k"
    
    print("🚀 Initializing Wikipedia 30k Chunking Pipeline")
    
    if not os.path.exists(raw_path):
        print(f"❌ Error: Raw data not found at {raw_path}")
        sys.exit(1)
        
    print(f"Loading dataset from {raw_path}...")
    dataset = load_from_disk(raw_path)
    print(f"Total documents to process: {len(dataset)}")
    
    all_chunks = []
    global_chunk_count = 0
    
    print("Processing and chunking...")
    for doc in dataset:
        doc_id = doc.get("id", "unknown")
        raw_text = doc.get("text", "")
        
        cleaned_text = clean_text(raw_text)
        text_chunks = chunk_text(cleaned_text)
        
        for i, chunk_content in enumerate(text_chunks):
            all_chunks.append({
                "text": chunk_content,
                "source_id": doc_id,
                "chunk_id": f"{doc_id}_{i}"
            })
            global_chunk_count += 1
            
    print(f"✅ Chunking complete!")
    print(f"Total chunks created: {global_chunk_count}")
    
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    chunked_dataset = Dataset.from_list(all_chunks)
    chunked_dataset.save_to_disk(processed_path)
    
if __name__ == "__main__":
    main()
