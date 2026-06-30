#!/usr/bin/env python3
"""Generate embeddings for the Freud Unified Database (including Kernberg positions)"""

import json
import os
import pickle
import glob
import numpy as np
from openai import OpenAI

def generate_embeddings():
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    db_path = 'data/FREUD_DATABASE_UNIFIED.json'
    print(f"Loading database from {db_path}...")
    
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    positions = db['positions']
    print(f"Total positions: {len(positions)}")
    
    old_embeddings = glob.glob('data/freud_unified_embeddings_*.pkl')
    if old_embeddings:
        print(f"Removing {len(old_embeddings)} old embedding files...")
        for f in old_embeddings:
            os.remove(f)
    
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(positions), batch_size):
        batch = positions[i:i+batch_size]
        texts = [p.get('text_evidence', p.get('text', '')) for p in batch]
        
        print(f"  Processing batch {i//batch_size + 1}/{(len(positions)-1)//batch_size + 1}...")
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    embeddings_array = np.array(all_embeddings)
    print(f"Generated {embeddings_array.shape[0]} embeddings")
    
    part_size = 1000
    chunk_size = 250
    base_path = 'data/freud_unified_embeddings'
    
    part_num = 1
    for part_start in range(0, len(embeddings_array), part_size):
        part_end = min(part_start + part_size, len(embeddings_array))
        part_data = embeddings_array[part_start:part_end]
        
        chunk_num = 1
        for chunk_start in range(0, len(part_data), chunk_size):
            chunk_end = min(chunk_start + chunk_size, len(part_data))
            chunk = part_data[chunk_start:chunk_end]
            
            chunk_path = f"{base_path}_part{part_num}_chunk{chunk_num}.pkl"
            with open(chunk_path, 'wb') as f:
                pickle.dump(chunk, f)
            print(f"Saved {chunk_path} ({len(chunk)} embeddings)")
            chunk_num += 1
        
        part_num += 1
    
    print(f"\nDone! Generated embeddings for {len(all_embeddings)} positions")

if __name__ == '__main__':
    generate_embeddings()
