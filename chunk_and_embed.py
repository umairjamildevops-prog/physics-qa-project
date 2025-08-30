# scripts/chunk_and_embed.py
# Usage: python chunk_and_embed.py ../data/physics_book.txt ../data/chunks.jsonl

import json
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i:i+chunk_size]
        chunks.append(" ".join(chunk_words))
        i += chunk_size - overlap
    return chunks

if __name__ == "__main__":
    import sys
    txt_path = sys.argv[1]
    out_path = sys.argv[2]
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, chunk_size=200, overlap=40)  # adjust for PDF density
    model = SentenceTransformer(MODEL_NAME)
    print("Generating embeddings...")
    with open(out_path, "w", encoding="utf-8") as fout:
        for i, ch in enumerate(tqdm(chunks)):
            emb = model.encode(ch).tolist()
            record = {"id": f"chunk_{i}", "text": ch, "embedding": emb}
            fout.write(json.dumps(record, ensure_ascii=False) + "\n")
    print("Wrote chunks+embeddings to", out_path)
