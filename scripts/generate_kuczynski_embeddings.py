#!/usr/bin/env python3
"""Generate embeddings for the Kuczynski Database"""

import json
import os
import pickle
import glob
import numpy as np
from openai import OpenAI

def generate_embeddings():
    client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
    
    db_path = 'data/KUCZYNSKI_COMPREHENSIVE_DATABASE.json'
    print(f"Loading database from {db_path}...")
    
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    positions = db['positions']
    print(f"Total positions: {len(positions)}")
    
    old_embeddings = glob.glob('data/KUCZYNSKI_COMPREHENSIVE_EMBEDDINGS*.pkl')
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
    
    output_path = 'data/KUCZYNSKI_COMPREHENSIVE_EMBEDDINGS.pkl'
    with open(output_path, 'wb') as f:
        pickle.dump(embeddings_array, f)
    print(f"Saved embeddings to {output_path}")
    
    print(f"\nDone! Generated embeddings for {len(all_embeddings)} positions")

if __name__ == '__main__':
    generate_embeddings()
