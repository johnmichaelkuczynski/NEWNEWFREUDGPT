import os
import json
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ.get('DATABASE_URL')

DATABASE_FILES = {
    'freud': 'data/FREUD_DATABASE_UNIFIED.json',
    'jung': 'data/JUNG_DATABASE.json',
    'kuczynski': 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json',
    'hume': 'data/HUME_DATABASE.json',
    'nietzsche': 'data/NIETZSCHE_DATABASE.json',
    'bergler': 'data/BERGLER_DATABASE.json'
}

def load_json_database(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if isinstance(data, dict):
        if 'positions' in data:
            return data['positions']
        elif 'database_metadata' in data:
            positions = []
            for key, value in data.items():
                if key not in ['database_metadata', 'metadata'] and isinstance(value, list):
                    positions.extend(value)
            if not positions:
                for key, value in data.items():
                    if isinstance(value, dict) and 'positions' in value:
                        positions.extend(value['positions'])
            return positions
    elif isinstance(data, list):
        return data
    return []

def extract_position_data(pos, thinker):
    position_id = pos.get('position_id') or pos.get('id') or ''
    title = pos.get('title') or pos.get('topic') or ''
    text_evidence = pos.get('text_evidence') or pos.get('text') or pos.get('position') or title
    domain = pos.get('domain') or ''
    source = pos.get('source', [])
    if isinstance(source, list):
        source = ', '.join(source) if source else ''
    work_title = pos.get('work_title') or pos.get('work') or ''
    year = pos.get('year')
    if year and not isinstance(year, int):
        try:
            year = int(year)
        except:
            year = None
    return (position_id, thinker, title, text_evidence, domain, source, work_title, year)

def migrate_database():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    total_inserted = 0
    
    for thinker, filepath in DATABASE_FILES.items():
        if not os.path.exists(filepath):
            print(f"⚠️  Skipping {thinker}: file not found ({filepath})")
            continue
            
        print(f"\n📚 Processing {thinker}...")
        positions = load_json_database(filepath)
        print(f"   Loaded {len(positions)} positions from JSON")
        
        if not positions:
            print(f"   ⚠️  No positions found in {filepath}")
            continue
        
        records = []
        for pos in positions:
            try:
                record = extract_position_data(pos, thinker)
                if record[0] and record[3]:
                    records.append(record)
            except Exception as e:
                print(f"   ⚠️  Error processing position: {e}")
        
        print(f"   Prepared {len(records)} valid records for insertion")
        
        if records:
            try:
                execute_values(
                    cur,
                    """INSERT INTO positions (position_id, thinker, title, text_evidence, domain, source, work_title, year)
                       VALUES %s
                       ON CONFLICT (position_id) DO UPDATE SET
                           title = EXCLUDED.title,
                           text_evidence = EXCLUDED.text_evidence,
                           domain = EXCLUDED.domain,
                           source = EXCLUDED.source,
                           work_title = EXCLUDED.work_title,
                           year = EXCLUDED.year""",
                    records,
                    page_size=1000
                )
                conn.commit()
                total_inserted += len(records)
                print(f"   ✓ Inserted/updated {len(records)} positions")
            except Exception as e:
                print(f"   ✗ Error inserting {thinker}: {e}")
                conn.rollback()
    
    cur.execute("SELECT thinker, COUNT(*) FROM positions GROUP BY thinker ORDER BY thinker")
    counts = cur.fetchall()
    
    print(f"\n{'='*50}")
    print("📊 MIGRATION COMPLETE")
    print(f"{'='*50}")
    print(f"Total positions migrated: {total_inserted}")
    print("\nPositions by thinker:")
    for thinker, count in counts:
        print(f"  {thinker}: {count}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    migrate_database()
