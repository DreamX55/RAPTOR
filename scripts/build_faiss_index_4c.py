import os
import json
import gc
import numpy as np
import faiss
from datasets import load_from_disk
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import argparse

def save_index(embeddings, chunk_mapping, index_save_path, mapping_save_path):
    embedding_dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings)
    os.makedirs(os.path.dirname(index_save_path), exist_ok=True)
    os.makedirs(os.path.dirname(mapping_save_path), exist_ok=True)
    faiss.write_index(index, index_save_path)
    with open(mapping_save_path, "w", encoding="utf-8") as f:
        json.dump(chunk_mapping, f, ensure_ascii=False, indent=2)
    print(f"✅ Saved index to {index_save_path} (size: {index.ntotal})")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", required=True)
    args = parser.parse_args()
    cat = args.category
    
    print("Loading SentenceTransformer model 'all-MiniLM-L6-v2'...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    batch_size = 128

    print("\n--- Reconstructing Clean Embeddings from FAISS ---")
    clean_index_path = "data/processed/faiss_index_15k.index"
    clean_mapping_path = "data/processed/chunk_mapping_15k.json"
    clean_index = faiss.read_index(clean_index_path)
    clean_embeddings = clean_index.reconstruct_n(0, clean_index.ntotal)
    with open(clean_mapping_path, "r", encoding="utf-8") as f:
        clean_mapping_list = json.load(f)
    clean_emb_dict = {mapping["chunk_id"]: emb for mapping, emb in zip(clean_mapping_list, clean_embeddings)}
    del clean_index, clean_embeddings, clean_mapping_list
    gc.collect()

    print(f"\n--- Processing Targeted Dataset for {cat} ---")
    attacked_path = f"data/processed/wikipedia_chunks_15k_{cat}"
    attacked_ds = load_from_disk(attacked_path)
    
    is_attack = [cid.startswith(f'attack_doc_{cat}_') for cid in attacked_ds['chunk_id']]
    attack_texts = [t for t, is_atk in zip(attacked_ds['text'], is_attack) if is_atk]
    attack_chunk_ids = [cid for cid, is_atk in zip(attacked_ds['chunk_id'], is_attack) if is_atk]
    
    attack_embeddings_list = []
    if len(attack_texts) > 0:
        for i in tqdm(range(0, len(attack_texts), batch_size), desc="Embedding Attack Chunks"):
            batch_texts = attack_texts[i:i+batch_size]
            embs = model.encode(batch_texts, batch_size=len(batch_texts), show_progress_bar=False)
            attack_embeddings_list.append(embs)
        attack_embeddings = np.vstack(attack_embeddings_list).astype('float32')
    else:
        attack_embeddings = np.array([], dtype='float32').reshape(0, 384)
        
    attack_emb_dict = {cid: emb for cid, emb in zip(attack_chunk_ids, attack_embeddings)}
    
    merged_embeddings = []
    merged_mapping = []
    for i in tqdm(range(len(attacked_ds)), desc="Merging Embeddings"):
        cid = attacked_ds["chunk_id"][i]
        sid = attacked_ds["source_id"][i]
        text = attacked_ds["text"][i]
        if cid.startswith(f'attack_doc_{cat}_'):
            merged_embeddings.append(attack_emb_dict[cid])
        else:
            merged_embeddings.append(clean_emb_dict[cid])
        merged_mapping.append({"chunk_id": cid, "source_id": sid, "text": text})
        
    merged_embeddings = np.array(merged_embeddings).astype('float32')
    
    del clean_emb_dict, attack_emb_dict, attack_embeddings_list, attack_embeddings
    gc.collect()
    
    save_index(
        merged_embeddings, 
        merged_mapping, 
        f"data/processed/faiss_index_{cat}.index", 
        f"data/processed/chunk_mapping_{cat}.json"
    )

if __name__ == "__main__":
    main()
