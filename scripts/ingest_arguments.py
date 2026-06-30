#!/usr/bin/env python3
"""
Ingest argument statements into PostgreSQL database.
Parses the structured argument format and stores for RAG retrieval.
"""

import os
import re
import json
import psycopg2
from datetime import datetime

DATABASE_URL = os.environ.get('DATABASE_URL')

def create_arguments_table():
    """Create the arguments table if it doesn't exist."""
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS arguments (
                id SERIAL PRIMARY KEY,
                author VARCHAR(100) NOT NULL,
                argument_number INTEGER NOT NULL,
                argument_type VARCHAR(50),
                section VARCHAR(500),
                premises TEXT[],
                conclusion TEXT NOT NULL,
                source VARCHAR(500),
                importance INTEGER,
                full_text TEXT,
                source_file VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(author, source_file, argument_number)
            );
            
            CREATE INDEX IF NOT EXISTS idx_arguments_author ON arguments(author);
            CREATE INDEX IF NOT EXISTS idx_arguments_section ON arguments(section);
            CREATE INDEX IF NOT EXISTS idx_arguments_fulltext ON arguments USING GIN(to_tsvector('english', full_text));
        """)
        conn.commit()
    conn.close()
    print("✓ Arguments table ready")

def parse_argument_file(filepath):
    """Parse an argument statements file and extract all arguments."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    arguments = []
    current_section = ""
    
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if line.startswith('## ') and not line.startswith('### '):
            current_section = line[3:].strip()
            i += 1
            continue
        
        arg_match = re.match(r'^### Argument (\d+)\s*\(([^)]+)\)', line)
        if arg_match:
            arg_num = int(arg_match.group(1))
            arg_type = arg_match.group(2).strip()
            
            i += 1
            author = ""
            premises = []
            conclusion = ""
            source = ""
            importance = None
            
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('### Argument ') or line.startswith('## '):
                    break
                
                if line.startswith('**Author:**'):
                    author = line.replace('**Author:**', '').strip()
                
                elif line.startswith('**Premises:**'):
                    i += 1
                    while i < len(lines):
                        prem_line = lines[i].strip()
                        if prem_line.startswith('- '):
                            premises.append(prem_line[2:].strip())
                            i += 1
                        elif prem_line.startswith('**→') or prem_line == '' or prem_line.startswith('*Source'):
                            break
                        else:
                            i += 1
                    continue
                
                elif line.startswith('**→ Conclusion:**') or line.startswith('**→Conclusion:**'):
                    conclusion = line.replace('**→ Conclusion:**', '').replace('**→Conclusion:**', '').strip()
                
                elif line.startswith('*Source:'):
                    source_match = re.match(r'\*Source:\s*([^|]+)\|\s*Importance:\s*(\d+)/10\*', line)
                    if source_match:
                        source = source_match.group(1).strip()
                        importance = int(source_match.group(2))
                
                i += 1
            
            if conclusion:
                full_text = f"[{arg_type.upper()}] "
                if premises:
                    full_text += "PREMISES: " + " | ".join(premises) + " "
                full_text += "THEREFORE: " + conclusion
                
                arguments.append({
                    'author': author.lower() if author else 'unknown',
                    'argument_number': arg_num,
                    'argument_type': arg_type,
                    'section': current_section,
                    'premises': premises,
                    'conclusion': conclusion,
                    'source': source,
                    'importance': importance,
                    'full_text': full_text
                })
        else:
            i += 1
    
    return arguments

def insert_arguments(arguments, source_file):
    """Insert parsed arguments into the database."""
    conn = psycopg2.connect(DATABASE_URL)
    inserted = 0
    updated = 0
    
    with conn.cursor() as cur:
        for arg in arguments:
            try:
                cur.execute("""
                    INSERT INTO arguments 
                    (author, argument_number, argument_type, section, premises, conclusion, source, importance, full_text, source_file)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (author, source_file, argument_number) 
                    DO UPDATE SET 
                        argument_type = EXCLUDED.argument_type,
                        section = EXCLUDED.section,
                        premises = EXCLUDED.premises,
                        conclusion = EXCLUDED.conclusion,
                        source = EXCLUDED.source,
                        importance = EXCLUDED.importance,
                        full_text = EXCLUDED.full_text
                    RETURNING (xmax = 0) AS inserted
                """, (
                    arg['author'],
                    arg['argument_number'],
                    arg['argument_type'],
                    arg['section'],
                    arg['premises'],
                    arg['conclusion'],
                    arg['source'],
                    arg['importance'],
                    arg['full_text'],
                    source_file
                ))
                result = cur.fetchone()
                if result and result[0]:
                    inserted += 1
                else:
                    updated += 1
            except Exception as e:
                print(f"Error inserting argument {arg['argument_number']}: {e}")
                conn.rollback()
                continue
        
        conn.commit()
    conn.close()
    
    return inserted, updated

def ingest_file(filepath):
    """Main function to ingest a single argument file."""
    print(f"Parsing {filepath}...")
    arguments = parse_argument_file(filepath)
    print(f"Found {len(arguments)} arguments")
    
    if arguments:
        source_file = os.path.basename(filepath)
        inserted, updated = insert_arguments(arguments, source_file)
        print(f"✓ Inserted: {inserted}, Updated: {updated}")
    
    return arguments

def get_argument_stats():
    """Get statistics about stored arguments."""
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cur:
        cur.execute("""
            SELECT author, COUNT(*) as count, 
                   COUNT(DISTINCT section) as sections,
                   COUNT(DISTINCT source_file) as files
            FROM arguments 
            GROUP BY author 
            ORDER BY count DESC
        """)
        stats = cur.fetchall()
    conn.close()
    return stats

if __name__ == '__main__':
    import sys
    
    create_arguments_table()
    
    if len(sys.argv) > 1:
        for filepath in sys.argv[1:]:
            if os.path.exists(filepath):
                ingest_file(filepath)
            else:
                print(f"File not found: {filepath}")
    else:
        print("Usage: python ingest_arguments.py <filepath> [filepath2 ...]")
        print("\nCurrent stats:")
        for author, count, sections, files in get_argument_stats():
            print(f"  {author}: {count} arguments, {sections} sections, {files} files")
