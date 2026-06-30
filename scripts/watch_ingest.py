#!/usr/bin/env python3
"""
File watcher for automatic ingestion.
Monitors the 'ingest' folder and processes new files automatically.
"""

import os
import sys
import time
import subprocess
import shutil
from pathlib import Path

INGEST_FOLDER = Path("ingest")
PROCESSED_FOLDER = Path("ingest/processed")
FAILED_FOLDER = Path("ingest/failed")
CHECK_INTERVAL = 3

INGEST_FOLDER.mkdir(exist_ok=True)
PROCESSED_FOLDER.mkdir(exist_ok=True)
FAILED_FOLDER.mkdir(exist_ok=True)

SUPPORTED_EXTENSIONS = {'.txt', '.pdf', '.docx', '.doc', '.json'}

THINKER_PREFIXES = {
    'freud': 'freud',
    'kuczynski': 'kuczynski',
    'kuc': 'kuczynski',
    'zhi': 'kuczynski',
    'jung': 'jung',
    'hume': 'hume',
    'nietzsche': 'nietzsche',
    'bergler': 'bergler',
}

def detect_thinker(filepath):
    """Detect thinker from filename suffix. Format: title_thinker.ext e.g. 'AI and Philosophy_KUCZYNSKI.txt'"""
    name = filepath.stem.lower()
    parts = name.replace('-', '_').replace(' ', '_').split('_')
    last_part = parts[-1] if parts else ''
    if last_part in THINKER_PREFIXES:
        return THINKER_PREFIXES[last_part]
    return 'kuczynski'

def get_files_to_process():
    """Get list of files waiting to be processed."""
    files = []
    for item in INGEST_FOLDER.iterdir():
        if item.is_file() and item.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(item)
    return files

def extract_text(filepath):
    """Extract text from a file (txt, pdf, docx)."""
    ext = filepath.suffix.lower()
    if ext == '.txt':
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for enc in encodings:
            try:
                with open(filepath, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        return None
    elif ext == '.pdf':
        try:
            import PyPDF2
            with open(filepath, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                return '\n'.join(page.extract_text() or '' for page in reader.pages)
        except Exception as e:
            print(f"PDF extraction error: {e}")
            return None
    elif ext in {'.docx', '.doc'}:
        try:
            import docx
            doc = docx.Document(str(filepath))
            return '\n'.join(p.text for p in doc.paragraphs)
        except Exception as e:
            print(f"DOCX extraction error: {e}")
            return None
    return None

def ingest_text_to_db(text, thinker, source_file):
    """Chunk text and insert into text_chunks and positions tables."""
    import psycopg2
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: No DATABASE_URL set")
        return False

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()

    words = text.split()
    chunk_size = 500
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk_text = ' '.join(words[i:i+chunk_size])
        if len(chunk_text.strip()) > 50:
            chunks.append(chunk_text)

    for i, chunk in enumerate(chunks):
        cur.execute('INSERT INTO text_chunks (thinker, source_file, chunk_text, chunk_index) VALUES (%s, %s, %s, %s)',
                    (thinker, source_file, chunk, i))

    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 80]
    pos_count = 0
    for para in paragraphs:
        if len(para) < 100:
            continue
        if len(para) > 1000:
            para = para[:1000]
        topic = f"From: {source_file}"
        cur.execute('INSERT INTO positions (thinker, topic, position, created_at) VALUES (%s, %s, %s, NOW())',
                    (thinker, topic, para))
        pos_count += 1

    conn.commit()
    cur.close()
    conn.close()
    print(f"   📦 Added {len(chunks)} text chunks + {pos_count} positions for {thinker}")
    return True

def process_file(filepath):
    """Process a single file through the ingestion pipeline."""
    thinker = detect_thinker(filepath)
    print(f"\n{'='*60}")
    print(f"📄 Processing: {filepath.name}")
    print(f"👤 Thinker: {thinker}")
    print(f"{'='*60}")
    
    ext = filepath.suffix.lower()
    success = False
    
    try:
        if ext == '.json':
            result = subprocess.run(
                ['python', 'scripts/ingest_work_positions.py', str(filepath)],
                capture_output=True,
                text=True,
                timeout=300
            )
            print(result.stdout)
            if result.returncode == 0:
                success = True
            else:
                print(f"Error: {result.stderr}")
        else:
            text = extract_text(filepath)
            if text and len(text.strip()) > 100:
                success = ingest_text_to_db(text, thinker, filepath.name)
                if success:
                    texts_dir = Path("texts")
                    texts_dir.mkdir(exist_ok=True)
                    safe_name = filepath.stem.replace(' ', '_') + '.txt'
                    with open(texts_dir / safe_name, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"   📝 Also saved to texts/{safe_name}")
            else:
                print(f"   ❌ Could not extract text or file too short")
        
        if success:
            dest = PROCESSED_FOLDER / filepath.name
            counter = 1
            while dest.exists():
                dest = PROCESSED_FOLDER / f"{filepath.stem}_{counter}{filepath.suffix}"
                counter += 1
            shutil.move(str(filepath), str(dest))
            print(f"✅ Success! Moved to: {dest}")
        else:
            dest = FAILED_FOLDER / filepath.name
            shutil.move(str(filepath), str(dest))
            print(f"❌ Failed! Moved to: {dest}")
            
    except subprocess.TimeoutExpired:
        print(f"❌ Timeout processing {filepath.name}")
        dest = FAILED_FOLDER / filepath.name
        shutil.move(str(filepath), str(dest))
    except Exception as e:
        print(f"❌ Error processing {filepath.name}: {e}")
        dest = FAILED_FOLDER / filepath.name
        try:
            shutil.move(str(filepath), str(dest))
        except:
            pass

def main():
    print("="*60)
    print("📂 Automatic Ingestion Watcher")
    print("="*60)
    print(f"Watching folder: {INGEST_FOLDER.absolute()}")
    print(f"Supported files: {', '.join(SUPPORTED_EXTENSIONS)}")
    print(f"Check interval: {CHECK_INTERVAL} seconds")
    print(f"Processed files go to: {PROCESSED_FOLDER}")
    print(f"Failed files go to: {FAILED_FOLDER}")
    print("="*60)
    print("Waiting for files...")
    
    seen_files = set()
    
    while True:
        try:
            files = get_files_to_process()
            
            for f in files:
                if f.name in seen_files:
                    continue
                    
                file_size = f.stat().st_size
                time.sleep(1)
                if f.exists() and f.stat().st_size == file_size:
                    process_file(f)
                    seen_files.discard(f.name)
                else:
                    seen_files.add(f.name)
                    
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n\n👋 Watcher stopped.")
            break
        except Exception as e:
            print(f"Watcher error: {e}")
            time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
