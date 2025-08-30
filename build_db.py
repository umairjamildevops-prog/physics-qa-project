# scripts/build_db.py
# Usage: python scripts/build_db.py data/chunks.jsonl

import json
import chromadb
import sys
import os

def build(chunks_file):
    # New Chroma client (v1.x)
    client = chromadb.PersistentClient(path=".chromadb")
    # If you want to start fresh, you can delete the existing collection (optional)
    try:
        client.delete_collection("physics10")
    except Exception:
        pass

    collection = client.get_or_create_collection(name="physics10")

    ids, metadatas, embeddings = [], [], []
    with open(chunks_file, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            ids.append(rec["id"])
            metadatas.append({"text": rec["text"]})
            embeddings.append(rec["embedding"])

    collection.add(ids=ids, metadatas=metadatas, embeddings=embeddings)
    print("✅ DB built with", len(ids), "chunks at .chromadb/")
    # No explicit persist needed for PersistentClient

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/build_db.py data/chunks.jsonl")
        sys.exit(1)
    build(sys.argv[1])

