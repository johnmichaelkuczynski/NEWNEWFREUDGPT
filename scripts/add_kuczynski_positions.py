#!/usr/bin/env python3
"""
Script to parse and add new Kuczynski position statements to the database.
Parses numbered position statements from the attached files.
"""

import json
import re
import os
from datetime import datetime

def parse_position_statements(filepath):
    """Parse numbered position statements from a text file."""
    positions = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'^(\d+)\.\s+(.+?)(?=\n\d+\.\s|\n\n|\Z)'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    for num, text in matches:
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 10:
            positions.append({
                'number': int(num),
                'text': text
            })
    
    return positions

def categorize_position(text):
    """Determine the domain/category of a position based on its content."""
    text_lower = text.lower()
    
    if any(term in text_lower for term in ['mind', 'mental', 'physical', 'brain', 'consciousness', 'dualism', 'materialism', 'qualia']):
        return 'philosophy_of_mind'
    elif any(term in text_lower for term in ['proposition', 'sentence', 'meaning', 'semantic', 'language', 'expression', 'predicate', 'reference']):
        return 'philosophy_of_language'
    elif any(term in text_lower for term in ['empiricism', 'knowledge', 'perception', 'epistem', 'belief', 'justif', 'a priori']):
        return 'epistemology'
    elif any(term in text_lower for term in ['logic', 'entail', 'valid', 'inference', 'argument', 'contradict', 'tautolog']):
        return 'logic'
    elif any(term in text_lower for term in ['property', 'universal', 'particular', 'exist', 'identity', 'cause', 'time', 'space', 'entity', 'object']):
        return 'metaphysics'
    elif any(term in text_lower for term in ['wittgenstein', 'russell', 'frege', 'chomsky', 'hume', 'kant', 'quine']):
        return 'history_of_philosophy'
    elif any(term in text_lower for term in ['psycholog', 'unconscious', 'conscious', 'emotion', 'feeling', 'think', 'cognit']):
        return 'psychology'
    elif any(term in text_lower for term in ['moral', 'ethical', 'value', 'good', 'right', 'virtue']):
        return 'ethics'
    else:
        return 'philosophy'

def create_position_entry(idx, text, source_work, prefix):
    """Create a position entry in the database format."""
    domain = categorize_position(text)
    
    return {
        'position_id': f'{prefix}-{idx:03d}',
        'text': text,
        'thesis': text[:200] + '...' if len(text) > 200 else text,
        'title': text[:80] + '...' if len(text) > 80 else text,
        'domain': domain,
        'source': source_work,
        'year': 2004,
        'work_title': source_work
    }

def main():
    position_statements_file = 'attached_assets/Pasted-1-Empiricism-cannot-explain-observable-events-because-i_1765094837046.txt'
    
    print("Parsing position statements...")
    raw_positions = parse_position_statements(position_statements_file)
    print(f"Found {len(raw_positions)} raw position statements")
    
    positions = []
    seen_texts = set()
    
    for pos in raw_positions:
        text = pos['text']
        text_normalized = text.lower().strip()[:100]
        
        if text_normalized not in seen_texts and len(text) >= 20:
            seen_texts.add(text_normalized)
            positions.append(text)
    
    print(f"After deduplication: {len(positions)} unique positions")
    
    source_work = "A Quasi-Materialist, Quasi-Dualist Solution to the Mind-Body Problem"
    prefix = "QMQD"
    
    new_entries = []
    for idx, text in enumerate(positions, 1):
        entry = create_position_entry(idx, text, source_work, prefix)
        new_entries.append(entry)
    
    domain_counts = {}
    for entry in new_entries:
        domain = entry['domain']
        domain_counts[domain] = domain_counts.get(domain, 0) + 1
    
    print("\nDomain distribution:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"  {domain}: {count}")
    
    print(f"\nSample positions:")
    for entry in new_entries[:5]:
        print(f"  [{entry['position_id']}] ({entry['domain']}) {entry['text'][:100]}...")
    
    database_path = 'data/KUCZYNSKI_COMPREHENSIVE_DATABASE.json'
    print(f"\nLoading existing database: {database_path}")
    
    with open(database_path, 'r', encoding='utf-8') as f:
        db_data = json.load(f)
    
    if isinstance(db_data, dict) and 'positions' in db_data:
        existing_positions = db_data['positions']
    else:
        existing_positions = db_data
    
    print(f"Existing database has {len(existing_positions)} positions")
    
    existing_ids = {p.get('position_id', '') for p in existing_positions}
    existing_texts = {p.get('text', '')[:100].lower() for p in existing_positions}
    
    truly_new = []
    for entry in new_entries:
        if entry['position_id'] not in existing_ids and entry['text'][:100].lower() not in existing_texts:
            truly_new.append(entry)
    
    print(f"Truly new positions to add: {len(truly_new)}")
    
    updated_positions = existing_positions + truly_new
    
    backup_path = f"data/KUCZYNSKI_COMPREHENSIVE_DATABASE_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(db_data, f, indent=2, ensure_ascii=False)
    print(f"Created backup: {backup_path}")
    
    if isinstance(db_data, dict) and 'positions' in db_data:
        db_data['positions'] = updated_positions
        db_data['total_positions'] = len(updated_positions)
        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump(db_data, f, indent=2, ensure_ascii=False)
    else:
        with open(database_path, 'w', encoding='utf-8') as f:
            json.dump(updated_positions, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated database saved with {len(updated_positions)} total positions")
    print(f"Added {len(truly_new)} new positions")
    
    return len(truly_new), len(updated_positions)

if __name__ == '__main__':
    new_count, total_count = main()
    print(f"\n=== SUMMARY ===")
    print(f"New positions added: {new_count}")
    print(f"Total positions now: {total_count}")
