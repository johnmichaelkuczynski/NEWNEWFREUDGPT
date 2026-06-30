import os
import re
import psycopg2
from psycopg2.extras import execute_values

DATABASE_URL = os.environ.get('DATABASE_URL')

TEXTS_DIR = 'texts'
CHUNK_SIZE = 500

THINKER_MAPPING = {
    'freud': ['freud/'],
    'kuczynski': [
        'A_Priori_Knowledge',
        'Analytic_Philosophy',
        'Attachment_Theory',
        'Chomskys_Two',
        'Conception_and_Causation',
        'Counterfactuals',
        'Dialogue_Concerning',
        'Dialogues_with_the_Master',
        'Group_Psychology',
        'Incompleteness',
        'Intensionality',
        'Kant_and_Hume',
        'King_Follett',
        'Libets_Experiment',
        'Logic_Set_Theory',
        'Mind_Meaning',
        'Moral_Structure',
        'Network_Reinterpretation',
        'Ninety_Paradoxes',
        'OCD_and_Philosophy',
        'Outline_of_a_Theory',
        'Papers_on_Accounting',
        'Philosophical_Knowledge',
        'Quantifiers',
        'Theoretical_Knowledge',
        'Three_Kinds_of_Psychopaths',
        'Why_Was_Socrates'
    ],
    'jung': ['jung/'],
    'hume': ['hume/'],
    'nietzsche': ['nietzsche/'],
    'bergler': ['bergler/']
}

def identify_thinker(filepath):
    for thinker, patterns in THINKER_MAPPING.items():
        for pattern in patterns:
            if pattern in filepath:
                return thinker
    return 'kuczynski'

def chunk_text(text, chunk_size=500):
    words = text.split()
    chunks = []
    current_chunk = []
    current_count = 0
    
    for word in words:
        current_chunk.append(word)
        current_count += 1
        
        if current_count >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_count = 0
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def clean_text(text):
    text = text.replace('\x00', '')
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def process_all_texts():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("DELETE FROM text_chunks")
    conn.commit()
    print("Cleared existing chunks")
    
    all_records = []
    files_processed = 0
    
    for root, dirs, files in os.walk(TEXTS_DIR):
        for filename in files:
            if not filename.endswith('.txt'):
                continue
                
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, TEXTS_DIR)
            thinker = identify_thinker(relative_path)
            
            print(f"Processing: {relative_path} -> {thinker}")
            
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except Exception as e:
                print(f"  Error reading file: {e}")
                continue
            
            content = clean_text(content)
            if len(content) < 100:
                print(f"  Skipping (too short)")
                continue
            
            chunks = chunk_text(content, CHUNK_SIZE)
            print(f"  Created {len(chunks)} chunks")
            
            for idx, chunk in enumerate(chunks):
                all_records.append((thinker, relative_path, chunk, idx))
            
            files_processed += 1
    
    if all_records:
        print(f"\nInserting {len(all_records)} chunks into database...")
        execute_values(
            cur,
            "INSERT INTO text_chunks (thinker, source_file, chunk_text, chunk_index) VALUES %s",
            all_records,
            page_size=500
        )
        conn.commit()
        print("Done!")
    
    cur.execute("SELECT thinker, COUNT(*) FROM text_chunks GROUP BY thinker ORDER BY thinker")
    counts = cur.fetchall()
    
    print(f"\n{'='*50}")
    print("CHUNKING COMPLETE")
    print(f"{'='*50}")
    print(f"Files processed: {files_processed}")
    print(f"Total chunks: {len(all_records)}")
    print("\nChunks by thinker:")
    for thinker, count in counts:
        print(f"  {thinker}: {count}")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    process_all_texts()
