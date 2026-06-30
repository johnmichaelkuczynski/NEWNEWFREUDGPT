#!/usr/bin/env python3
"""Generate embeddings for Hume database."""
import json
import pickle
import os
from openai import OpenAI

client = OpenAI()
DB_PATH = "data/HUME_DATABASE.json"
EMB_PATH = "data/hume_embeddings.pkl"

def main():
    print(f"Loading database from {DB_PATH}...")
    with open(DB_PATH, 'r') as f:
        positions = json.load(f)
    print(f"Total positions: {len(positions)}")
    
    for old in os.listdir("data"):
        if old.startswith("hume") and old.endswith(".pkl"):
            os.remove(f"data/{old}")
            print(f"Removed old: {old}")
    
    embeddings = {}
    batch_size = 100
    total_batches = (len(positions) + batch_size - 1) // batch_size
    
    for i in range(0, len(positions), batch_size):
        batch = positions[i:i+batch_size]
        batch_num = i // batch_size + 1
        print(f"  Processing batch {batch_num}/{total_batches}...")
        
        texts = [p["text_evidence"][:8000] for p in batch]
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        for j, emb in enumerate(response.data):
            pos_id = batch[j]["id"]
            embeddings[pos_id] = emb.embedding
    
    print(f"Generated {len(embeddings)} embeddings")
    
    with open(EMB_PATH, 'wb') as f:
        pickle.dump(embeddings, f)
    print(f"Saved embeddings to {EMB_PATH}")
    
    print(f"\nDone! Generated embeddings for {len(positions)} positions")
    print(f"Database positions: {len(positions)}")
    print(f"Embeddings count: {len(embeddings)}")
    if len(positions) == len(embeddings):
        print("✓ Counts match!")
    else:
        print("✗ Count mismatch!")

if __name__ == "__main__":
    main()
