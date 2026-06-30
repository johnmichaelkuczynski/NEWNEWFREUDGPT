#!/usr/bin/env python3
"""Regenerate ALL Kuczynski embeddings to match current database exactly"""

import json
import os
import numpy as np
from openai import OpenAI

def regenerate_embeddings():
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    print(f"Loading database from {db_path}...")
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    positions = db['positions']
    print(f"Total positions in database: {len(positions)}")
    
    texts = []
    for p in positions:
        text = p.get('text', '') or p.get('thesis', '') or p.get('text_evidence', '') or p.get('title', '')
        if not text.strip():
            text = "Empty position placeholder"
        texts.append(text[:8000])
    
    print(f"Generating embeddings for {len(texts)} positions...")
    
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        print(f"  Processing batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}...")
        
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=batch
        )
        
        batch_embeddings = [item.embedding for item in response.data]
        all_embeddings.extend(batch_embeddings)
    
    embeddings_array = np.array(all_embeddings)
    print(f"Generated {embeddings_array.shape[0]} embeddings")
    
    output_path = 'data/kuczynski_embeddings.npy'
    backup_path = 'data/kuczynski_embeddings_old.npy'
    
    if os.path.exists(output_path):
        os.rename(output_path, backup_path)
        print(f"Backed up old embeddings to {backup_path}")
    
    np.save(output_path, embeddings_array)
    print(f"Saved new embeddings to {output_path}")
    
    print(f"\nDone! Embeddings now match database: {embeddings_array.shape[0]} embeddings for {len(positions)} positions")

if __name__ == '__main__':
    regenerate_embeddings()
