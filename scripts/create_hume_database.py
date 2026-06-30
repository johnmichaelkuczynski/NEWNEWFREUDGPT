#!/usr/bin/env python3
"""Create Hume database from position statements file"""

import json
import re
from datetime import datetime

def parse_hume_positions():
    """Parse the Hume positions file and extract all positions with metadata"""
    
    with open('attached_assets/Pasted-Here-are-25-key-positions-theses-arguments-or-philosoph_1765093457038.txt', 'r') as f:
        lines = f.readlines()
    
    positions = []
    
    works_metadata = {
        "A Treatise of Human Nature": {"year": 1739, "abbrev": "THN", "domain": "EPISTEMOLOGY_&_METAPHYSICS"},
        "An Enquiry concerning Human Understanding": {"year": 1748, "abbrev": "EHU", "domain": "EPISTEMOLOGY"},
        "An Enquiry concerning the Principles of Morals": {"year": 1751, "abbrev": "EPM", "domain": "ETHICS"},
        "Dialogues concerning Natural Religion": {"year": 1779, "abbrev": "DNR", "domain": "PHILOSOPHY_OF_RELIGION"},
        "Natural History of Religion": {"year": 1757, "abbrev": "NHR", "domain": "PHILOSOPHY_OF_RELIGION"},
        "History of England": {"year": 1754, "abbrev": "HOE", "domain": "POLITICAL_PHILOSOPHY"},
        "Political Essays": {"year": 1752, "abbrev": "PE", "domain": "POLITICAL_ECONOMY"}
    }
    
    current_work = "A Treatise of Human Nature"
    current_domain = "EPISTEMOLOGY_&_METAPHYSICS"
    in_natural_history = False
    
    section_headers = [
        "Origins of Religion", "Psychological Sources", "Role of Ignorance",
        "Anthropomorphism", "Polytheism and Its Character", "Rise of Monotheism",
        "Flux Between", "Comparison of Polytheism", "Religion and Morality",
        "Religion and Human Nature", "Constitutional Development", "Monarchy and Royal Power",
        "Parliament and Representation", "English Civil War", "Oliver Cromwell",
        "Religion and Politics", "Reformation", "Manners, Commerce"
    ]
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        if "### A Treatise of Human Nature" in line:
            current_work = "A Treatise of Human Nature"
            current_domain = "EPISTEMOLOGY_&_METAPHYSICS"
            in_natural_history = False
            continue
        elif "### An Enquiry concerning Human Understanding" in line:
            current_work = "An Enquiry concerning Human Understanding"
            current_domain = "EPISTEMOLOGY"
            in_natural_history = False
            continue
        elif "### An Enquiry concerning the Principles of Morals" in line:
            current_work = "An Enquiry concerning the Principles of Morals"
            current_domain = "ETHICS"
            in_natural_history = False
            continue
        elif "### Dialogues concerning Natural Religion" in line:
            current_work = "Dialogues concerning Natural Religion"
            current_domain = "PHILOSOPHY_OF_RELIGION"
            in_natural_history = False
            continue
        
        if "additional distinct positions" in line.lower() or "Here are 100" in line:
            if "Treatise of Human Nature" in line:
                current_work = "A Treatise of Human Nature"
                current_domain = "EPISTEMOLOGY_&_METAPHYSICS"
                in_natural_history = False
            elif "Enquiry concerning the Principles of Morals" in line:
                current_work = "An Enquiry concerning the Principles of Morals"
                current_domain = "ETHICS"
                in_natural_history = False
            elif "Enquiry concerning Human Understanding" in line:
                current_work = "An Enquiry concerning Human Understanding"
                current_domain = "EPISTEMOLOGY"
                in_natural_history = False
            elif "Natural History of Religion" in line:
                current_work = "Natural History of Religion"
                current_domain = "PHILOSOPHY_OF_RELIGION"
                in_natural_history = True
            elif "History of England" in line:
                current_work = "History of England"
                current_domain = "POLITICAL_PHILOSOPHY"
                in_natural_history = False
            continue
        
        if "HISTORY OF ENGLAND" in line or ("History of England" in line and "100 position" in line):
            current_work = "History of England"
            current_domain = "POLITICAL_PHILOSOPHY"
            in_natural_history = False
            continue
        
        is_section_header = any(header in line for header in section_headers)
        if is_section_header and len(line) < 50:
            if "Origins of Religion" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Psychological Sources" in line:
                current_domain = "PHILOSOPHY_OF_MIND"
            elif "Role of Ignorance" in line:
                current_domain = "EPISTEMOLOGY"
            elif "Anthropomorphism" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Polytheism" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Rise of Monotheism" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Flux Between" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Comparison of" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Religion and Morality" in line:
                current_domain = "ETHICS"
            elif "Religion and Human Nature" in line:
                current_domain = "PHILOSOPHY_OF_RELIGION"
            elif "Constitutional Development" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "Monarchy" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "Parliament" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "English Civil War" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "Oliver Cromwell" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "Religion and Politics" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "Reformation" in line:
                current_domain = "POLITICAL_PHILOSOPHY"
            elif "Manners, Commerce" in line:
                current_domain = "POLITICAL_ECONOMY"
            continue
        
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match:
            text = match.group(2).strip()
            if len(text) > 15:
                meta = works_metadata.get(current_work, {"year": 1750, "abbrev": "HUME", "domain": current_domain})
                positions.append({
                    "text": text,
                    "work": current_work,
                    "year": meta["year"],
                    "abbrev": meta["abbrev"],
                    "domain": current_domain
                })
        elif in_natural_history or current_work == "Natural History of Religion":
            if line and len(line) > 30 and line[0].isupper():
                skip_phrases = ["Here are", "additional", "Truncated", "cover its full scope", "Appendix", "These are new"]
                if not any(phrase in line for phrase in skip_phrases):
                    if '.' in line and not line.startswith('...') and not line.startswith('**'):
                        meta = works_metadata.get("Natural History of Religion")
                        positions.append({
                            "text": line,
                            "work": "Natural History of Religion",
                            "year": meta["year"],
                            "abbrev": meta["abbrev"],
                            "domain": current_domain
                        })
    
    return positions


def create_database():
    """Create the Hume database JSON file"""
    
    raw_positions = parse_hume_positions()
    
    seen_texts = set()
    unique_positions = []
    
    for pos in raw_positions:
        text_key = pos['text'].lower().strip()[:100]
        if text_key not in seen_texts and len(pos['text']) > 20:
            seen_texts.add(text_key)
            unique_positions.append(pos)
    
    final_positions = []
    work_counters = {}
    
    for pos in unique_positions:
        abbrev = pos['abbrev']
        work_counters[abbrev] = work_counters.get(abbrev, 0) + 1
        pos_id = f"{abbrev}-{work_counters[abbrev]:04d}"
        
        final_positions.append({
            "id": pos_id,
            "position_id": pos_id,
            "author": "David Hume",
            "title": pos['text'][:100] + ("..." if len(pos['text']) > 100 else ""),
            "text_evidence": pos['text'],
            "domain": pos['domain'],
            "work_id": f"WORK-{pos['work'].replace(' ', '_').upper()[:20]}",
            "work_title": pos['work'],
            "source": [pos['work']],
            "year": pos['year']
        })
    
    database = {
        "metadata": {
            "name": "Hume Philosophical Database",
            "version": "v1.0",
            "created": datetime.now().isoformat(),
            "description": f"David Hume's philosophical positions from major works. Total: {len(final_positions)} positions.",
            "total_positions": len(final_positions),
            "last_updated": datetime.now().strftime("%Y-%m-%d"),
            "works_included": [
                "A Treatise of Human Nature (1739-1740)",
                "An Enquiry concerning Human Understanding (1748)",
                "An Enquiry concerning the Principles of Morals (1751)",
                "Dialogues concerning Natural Religion (1779)",
                "Natural History of Religion (1757)",
                "History of England (1754-1762)",
                "Political Essays (1752)"
            ]
        },
        "positions": final_positions
    }
    
    output_path = 'data/HUME_DATABASE.json'
    with open(output_path, 'w') as f:
        json.dump(database, f, indent=2)
    
    print(f"Created Hume database with {len(final_positions)} unique positions")
    print(f"Saved to: {output_path}")
    
    works_count = {}
    for pos in final_positions:
        work = pos['work_title']
        works_count[work] = works_count.get(work, 0) + 1
    
    print("\nPositions by work:")
    for work, count in sorted(works_count.items(), key=lambda x: -x[1]):
        print(f"  {work}: {count}")
    
    print(f"\nSample positions:")
    samples = [0, 100, 300, 500, 700, 900]
    for i in samples:
        if i < len(final_positions):
            p = final_positions[i]
            print(f"  [{p['id']}] {p['work_title']}: {p['text_evidence'][:70]}...")
    
    return len(final_positions)


if __name__ == '__main__':
    create_database()
