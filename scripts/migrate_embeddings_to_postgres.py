#!/usr/bin/env python3
"""Migrate embeddings from pkl files to PostgreSQL database"""

import os
import json
import pickle
import glob
import numpy as np
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ.get('DATABASE_URL')

THINKER_CONFIG = {
    'kuczynski': {
        'db_path': 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json',
        'embedding_pattern': 'data/kuczynski_v42_embeddings*.pkl',
        'positions_key': 'positions'
    },
    'freud': {
        'db_path': 'data/FREUD_DATABASE_UNIFIED.json',
        'embedding_pattern': 'data/freud_unified_embeddings*.pkl',
        'positions_key': 'positions'
    },
    'jung': {
        'db_path': 'data/JUNG_DATABASE.json',
        'embedding_pattern': 'data/jung_embeddings*.pkl',
        'positions_key': 'positions'
    },
    'hume': {
        'db_path': 'data/HUME_DATABASE.json',
        'embedding_pattern': 'data/hume_embeddings*.pkl',
        'positions_key': None
    },
    'nietzsche': {
        'db_path': 'data/NIETZSCHE_DATABASE.json',
        'embedding_pattern': 'data/nietzsche_embeddings*.pkl',
        'positions_key': 'positions'
    },
    'bergler': {
        'db_path': 'data/BERGLER_DATABASE.json',
        'embedding_pattern': 'data/bergler_embeddings*.pkl',
        'positions_key': 'positions'
    }
}

def load_embeddings(pattern):
    """Load embeddings from pkl files (handles split files)"""
    files = sorted(glob.glob(pattern))
    if not files:
        return None
    
    all_embeddings = []
    for f in files:
        with open(f, 'rb') as fp:
            data = pickle.load(fp)
            if isinstance(data, np.ndarray):
                all_embeddings.append(data)
            elif isinstance(data, list):
                all_embeddings.append(np.array(data))
    
    if not all_embeddings:
        return None
    
    return np.vstack(all_embeddings)

def load_positions(db_path, positions_key):
    """Load positions from JSON database"""
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    if positions_key:
        positions = db.get(positions_key, [])
    else:
        positions = db if isinstance(db, list) else db.get('positions', [])
    
    return positions

def migrate_thinker(conn, thinker, config):
    """Migrate a single thinker's embeddings to PostgreSQL"""
    print(f"\nMigrating {thinker}...")
    
    embeddings = load_embeddings(config['embedding_pattern'])
    if embeddings is None:
        print(f"  No embeddings found for {thinker}")
        return 0
    
    positions = load_positions(config['db_path'], config['positions_key'])
    
    print(f"  Embeddings: {embeddings.shape[0]}, Positions: {len(positions)}")
    
    if embeddings.shape[0] != len(positions):
        print(f"  WARNING: Mismatch! Using min count: {min(embeddings.shape[0], len(positions))}")
    
    count = min(embeddings.shape[0], len(positions))
    
    with conn.cursor() as cur:
        cur.execute("DELETE FROM position_embeddings WHERE thinker = %s", (thinker,))
        print(f"  Cleared existing embeddings for {thinker}")
        
        batch_size = 500
        inserted = 0
        
        for i in range(0, count, batch_size):
            batch_end = min(i + batch_size, count)
            batch_data = []
            
            for j in range(i, batch_end):
                pos = positions[j]
                pos_id = pos.get('id') or pos.get('position_id') or f"{thinker.upper()}-{j:05d}"
                embedding = embeddings[j].tolist()
                batch_data.append((pos_id, thinker, embedding))
            
            execute_values(
                cur,
                "INSERT INTO position_embeddings (position_id, thinker, embedding) VALUES %s",
                batch_data,
                template="(%s, %s, %s::vector)"
            )
            inserted += len(batch_data)
            print(f"  Inserted {inserted}/{count}...")
        
        conn.commit()
    
    return inserted

def main():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)
    
    total_migrated = 0
    
    for thinker, config in THINKER_CONFIG.items():
        try:
            count = migrate_thinker(conn, thinker, config)
            total_migrated += count
        except Exception as e:
            print(f"  ERROR migrating {thinker}: {e}")
            conn.rollback()
    
    conn.close()
    
    print(f"\n{'='*50}")
    print(f"Migration complete! Total embeddings migrated: {total_migrated}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
