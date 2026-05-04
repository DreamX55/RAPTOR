import os
import re
import sys
from datasets import load_from_disk, Dataset

def clean_text(text):
    """
    Removes markup tags and cleans whitespace from the text.
    """
    if not text:
        return ""
    # Remove HTML-like tags (e.g., <H1>, <P>, <Table>)
    text = re.sub(r'<[^>]+>', '', text)
    # Normalize whitespace (replace newlines/tabs with spaces)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_into_sentences(text):
    """
    Splits text into sentences using a regex pattern.
    """
    # Simple regex for sentence splitting that handles common abbreviations
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def chunk_text(text, target_words=250, min_words=100):
    """
    Splits text into semantic chunks of ~200-300 words.
    """
    sentences = split_into_sentences(text)
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        words = sentence.split()
        count = len(words)
        
        # If adding this sentence exceeds target, and we have enough words, finalize chunk
        if current_word_count + count > 300: # Upper limit
            if current_word_count >= min_words:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                current_word_count = 0
        
        current_chunk.append(sentence)
        current_word_count += count
        
    # Handle the last remaining chunk
    if current_chunk:
        chunk_str = " ".join(current_chunk).strip()
        if len(chunk_str.split()) >= min_words:
            chunks.append(chunk_str)
        elif chunks:
            # If last chunk is too small, append it to the previous one
            chunks[-1] += " " + chunk_str
        else:
            # If doc is small overall, just keep it as one chunk
            chunks.append(chunk_str)
            
    return chunks

def main():
    raw_path = "data/raw/wikipedia"
    processed_path = "data/processed/wikipedia_chunks"
    
    print("🚀 Initializing Wikipedia Chunking Pipeline")
    
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
        
        # 1. Clean
        cleaned_text = clean_text(raw_text)
        
        # 2. Chunk
        text_chunks = chunk_text(cleaned_text)
        
        # 3. Format
        for i, chunk_content in enumerate(text_chunks):
            all_chunks.append({
                "text": chunk_content,
                "source_id": doc_id,
                "chunk_id": f"{doc_id}_{i}"
            })
            global_chunk_count += 1
            
    print(f"✅ Chunking complete!")
    print(f"Total chunks created: {global_chunk_count}")
    
    # Save as HuggingFace Dataset
    print(f"Saving to {processed_path}...")
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    chunked_dataset = Dataset.from_list(all_chunks)
    chunked_dataset.save_to_disk(processed_path)
    
    # Preview
    if all_chunks:
        print("\n--- Sample Chunk Preview ---")
        sample = all_chunks[0]
        print(f"Source ID: {sample['source_id']}")
        print(f"Chunk ID:  {sample['chunk_id']}")
        print(f"Content (first 200 chars): {sample['text'][:200]}...")
        print(f"Word count: {len(sample['text'].split())}")

if __name__ == "__main__":
    main()
