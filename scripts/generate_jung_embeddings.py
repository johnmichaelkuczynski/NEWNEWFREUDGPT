#!/usr/bin/env python3
"""Generate embeddings for the Jung Database"""

import json
import os
import pickle
import glob
import numpy as np
from openai import OpenAI

def generate_embeddings():
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    db_path = 'data/JUNG_DATABASE.json'
    print(f"Loading database from {db_path}...")
    
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    positions = db['positions']
    print(f"Total positions: {len(positions)}")
    
    old_embeddings = glob.glob('data/jung_embeddings*.pkl')
    if old_embeddings:
        print(f"Removing {len(old_embeddings)} old embedding files...")
        for f in old_embeddings:
            os.remove(f)
    
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(positions), batch_size):
        batch = positions[i:i+batch_size]
        texts = []
        for p in batch:
            text = p.get('thesis', '') or p.get('text', '') or p.get('title', '')
            if p.get('key_arguments'):
                text = text + " " + " ".join(p['key_arguments'][:2])
            texts.append(text)
        
        print(f"  Processing batch {i//batch_size + 1}/{(len(positions)-1)//batch_size + 1}...")
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    embeddings_array = np.array(all_embeddings)
    print(f"Generated {embeddings_array.shape[0]} embeddings")
    
    output_path = 'data/jung_embeddings.pkl'
    with open(output_path, 'wb') as f:
        pickle.dump(embeddings_array, f)
    print(f"Saved embeddings to {output_path}")
    
    print(f"\nDone! Generated embeddings for {len(all_embeddings)} positions")
    print(f"Database positions: {len(positions)}")
    print(f"Embeddings count: {embeddings_array.shape[0]}")
    
    if len(positions) == embeddings_array.shape[0]:
        print("✓ Counts match!")
    else:
        print("⚠️  WARNING: Count mismatch!")

if __name__ == '__main__':
    generate_embeddings()
