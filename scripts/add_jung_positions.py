#!/usr/bin/env python3
"""
Script to add new Jung position statements from text file to JUNG_DATABASE.json
"""

import json
import re
from pathlib import Path

def parse_positions_file(file_path):
    """Parse the positions file and extract positions with categories."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = re.split(r'={80}\n([A-Z][A-Z\s:,\-]+)\n={80}', content)
    
    positions = []
    current_category = None
    
    for i, section in enumerate(sections):
        section = section.strip()
        if not section:
            continue
        
        if re.match(r'^[A-Z][A-Z\s:,\-]+$', section):
            current_category = section.title()
            continue
        
        if current_category:
            lines = section.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('* '):
                    position_text = line[2:].strip()
                    if position_text:
                        positions.append({
                            'category': current_category,
                            'text': position_text
                        })
    
    return positions

def add_positions_to_database(positions, db_path, output_path=None):
    """Add positions to the Jung database."""
    if output_path is None:
        output_path = db_path
    
    with open(db_path, 'r', encoding='utf-8') as f:
        db = json.load(f)
    
    existing_positions = db.get('positions', [])
    existing_count = len(existing_positions)
    
    new_positions = []
    for idx, pos in enumerate(positions, start=1):
        position_id = f"JUNG-NEW-{idx:03d}"
        new_position = {
            "position_id": position_id,
            "title": pos['text'][:100] + "..." if len(pos['text']) > 100 else pos['text'],
            "source": ["Additional Jung Position Statements"],
            "thesis": pos['text'],
            "work_code": "APS",
            "work_title": "Additional Position Statements",
            "domain": pos['category'],
            "consistency": "Core to Jung's view",
            "key_arguments": [pos['text']]
        }
        new_positions.append(new_position)
    
    db['positions'] = existing_positions + new_positions
    
    if 'database_metadata' in db:
        db['database_metadata']['total_positions'] = len(db['positions'])
        db['database_metadata']['expansion_date'] = "2025-12-08"
        db['database_metadata']['expansion_note'] = f"Added {len(new_positions)} positions from Additional Jung Position Statements"
    
    if 'metadata' in db:
        db['metadata']['total_positions'] = len(db['positions'])
        db['metadata']['last_updated'] = "2025-12-08"
        db['metadata']['batch5_expansion'] = f"Added {len(new_positions)} additional position statements"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    return len(new_positions), len(db['positions'])


def main():
    positions_file = Path("attached_assets/Pasted-ADDITIONAL-JUNG-POSITION-STATEMENTS--1765171475557_1765171475558.txt")
    db_path = Path("data/JUNG_DATABASE.json")
    
    print("Parsing positions file...")
    positions = parse_positions_file(positions_file)
    print(f"Found {len(positions)} positions")
    
    categories = {}
    for pos in positions:
        cat = pos['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\nPositions by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")
    
    print("\nAdding positions to database...")
    added, total = add_positions_to_database(positions, db_path)
    print(f"Added {added} new positions. Total positions: {total}")


if __name__ == "__main__":
    main()
