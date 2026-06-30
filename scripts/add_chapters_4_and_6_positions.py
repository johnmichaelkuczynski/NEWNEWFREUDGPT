#!/usr/bin/env python3
"""
Add Chapter 4 (What Is a Language?) and Chapter 6 (Russell's Improvements on Frege's Work)
positions to the Kuczynski database.

Fixed version addressing:
- Unique position_id with chapter prefix (kuc-hmw-ch4-XXX, kuc-hmw-ch6-XXX)
- Distinct work_id for each chapter
- Verbatim quotes preserved
- Enhanced keyword extraction
- Proper section mapping
"""

import json
import re

CHAPTER_4_FILE = "attached_assets/Pasted--100-Positions-Extracted-from-Kuczynski-What-Is-a-Langu_1765108707055.txt"
CHAPTER_6_FILE = "attached_assets/Pasted--150-Positions-Extracted-from-Kuczynski-Russell-s-Impro_1765109418577.txt"
DATABASE_FILE = "data/KUCZYNSKI_COMPREHENSIVE_DATABASE.json"

CHAPTER_4_TOPICS = {
    "THE THREE MEANINGS OF \"MEANING\"": {
        "keywords": ["meaning", "evidential", "psychological", "linguistic", "semantics"],
        "topic": "philosophy of language"
    },
    "LANGUAGE AS CONVENTIONAL AND NORMATIVE": {
        "keywords": ["convention", "normative", "language", "utterance"],
        "topic": "philosophy of language"
    },
    "PROPOSITIONS AND SENTENCES": {
        "keywords": ["proposition", "sentence", "meaning", "truth"],
        "topic": "philosophy of language"
    },
    "PROPOSITIONS AS DIGITAL STRUCTURES": {
        "keywords": ["proposition", "digital", "structure", "morpheme", "analogue"],
        "topic": "philosophy of language"
    },
    "THE THREE BRANCHES: SEMANTICS, SYNTAX, PRAGMATICS": {
        "keywords": ["semantics", "syntax", "pragmatics", "literal meaning"],
        "topic": "philosophy of language"
    },
    "THE NEED FOR SEMANTICS": {
        "keywords": ["semantics", "logical form", "meaning", "analysis"],
        "topic": "philosophy of language"
    },
    "SEMANTIC RULES: WHAT THEY ARE": {
        "keywords": ["semantic rule", "language", "expression", "meaning"],
        "topic": "philosophy of language"
    },
    "AGAINST THE FUNCTION-THEORETIC VIEW": {
        "keywords": ["semantic rule", "function", "mathematical", "language"],
        "topic": "philosophy of language"
    },
    "AGAINST GRICE'S THEORY OF MEANING": {
        "keywords": ["Grice", "speaker meaning", "literal meaning", "compositional"],
        "topic": "history of philosophy"
    },
    "AGAINST WITTGENSTEIN'S \"MEANING IS USE\"": {
        "keywords": ["Wittgenstein", "meaning", "use", "expression"],
        "topic": "history of philosophy"
    },
    "AGAINST CONCEPTUAL ROLE SEMANTICS": {
        "keywords": ["CRS", "conceptual role", "Field", "Brandom", "inference"],
        "topic": "philosophy of language"
    },
    "THE NORMATIVITY AND PSYCHOLOGICAL REALITY": {
        "keywords": ["normative", "semantic rule", "psychological", "speaker"],
        "topic": "philosophy of language"
    },
    "LITERAL MEANING AND SIMPLE VS. COMPLEX": {
        "keywords": ["literal meaning", "simple expression", "complex expression"],
        "topic": "philosophy of language"
    },
    "TOKENS VS. TYPES": {
        "keywords": ["token", "type", "expression", "utterance", "inscription"],
        "topic": "philosophy of language"
    },
    "TWO-DIMENSIONAL SEMANTICS": {
        "keywords": ["two-dimensional", "indexical", "demonstrative", "context", "reference"],
        "topic": "philosophy of language"
    },
    "CONTEXT-SENSITIVITY": {
        "keywords": ["context-sensitive", "eternal sentence", "tense", "token"],
        "topic": "philosophy of language"
    },
    "LOGICAL FORM VS. GRAMMATICAL FORM": {
        "keywords": ["logical form", "grammatical form", "Frege", "quantifier"],
        "topic": "logic"
    }
}

CHAPTER_6_TOPICS = {
    "THE THEORY OF DESCRIPTIONS: CORE CLAIMS": {
        "keywords": ["Russell", "theory of descriptions", "definite description", "truth-conditions"],
        "topic": "philosophy of language"
    },
    "DEFINITE DESCRIPTIONS ARE NOT REFERRING TERMS": {
        "keywords": ["definite description", "reference", "contextual definition", "logical form"],
        "topic": "philosophy of language"
    },
    "THE ESSENCE OF TD": {
        "keywords": ["theory of descriptions", "property", "instantiation", "reference"],
        "topic": "philosophy of language"
    },
    "TD SOLVES THE PROBLEM OF BELIEF REPORTS": {
        "keywords": ["belief report", "theory of descriptions", "Meinong", "existence"],
        "topic": "philosophy of mind"
    },
    "TD SOLVES THE PROBLEM OF NEGATIVE EXISTENTIALS": {
        "keywords": ["negative existential", "existence", "property", "instantiation"],
        "topic": "metaphysics"
    },
    "REFERENCE: FUNDAMENTAL PRINCIPLES": {
        "keywords": ["reference", "proper name", "property", "attribution"],
        "topic": "philosophy of language"
    },
    "TD SOLVES THE PUZZLE OF INFORMATIVE IDENTITY STATEMENTS": {
        "keywords": ["identity", "informative", "trivial", "theory of descriptions"],
        "topic": "philosophy of language"
    },
    "TD SOLVES THE PUZZLE OF POSITIVE EXISTENTIALS": {
        "keywords": ["positive existential", "existence", "property", "instantiation"],
        "topic": "metaphysics"
    },
    "FREGE'S SENSE/REFERENCE DISTINCTION": {
        "keywords": ["Frege", "sense", "reference", "referent"],
        "topic": "history of philosophy"
    },
    "FREGE'S THEORY COLLAPSES INTO RUSSELL'S": {
        "keywords": ["Frege", "Russell", "theory of descriptions", "sense"],
        "topic": "history of philosophy"
    },
    "WHY FREGEANISM DOESN'T COMPLETELY COLLAPSE": {
        "keywords": ["Frege", "Russell", "referring term", "theory of descriptions"],
        "topic": "history of philosophy"
    },
    "THE SUBSTITUTION FAILURE ARGUMENT": {
        "keywords": ["substitution", "Leibniz's Law", "belief", "co-reference"],
        "topic": "philosophy of language"
    },
    "FREGE'S FAILED COVER-UP: INTENSIONAL CONTEXTS": {
        "keywords": ["intensional", "extensional", "substitution", "proposition"],
        "topic": "philosophy of language"
    },
    "FREGE'S FUNDAMENTAL CONFUSIONS": {
        "keywords": ["Frege", "reference", "quantification", "compositionality"],
        "topic": "history of philosophy"
    },
    "FREGE'S DESPERATE EPICYCLE: REFERENCE-SHIFTS": {
        "keywords": ["reference-shift", "intensional", "Frege", "operator"],
        "topic": "history of philosophy"
    },
    "SYNTACTIC AMBIGUITY AND THE WIDE-SCOPE/NARROW-SCOPE": {
        "keywords": ["scope", "ambiguity", "operator", "quantifier", "syntactic"],
        "topic": "philosophy of language"
    },
    "TD SOLVES QUINE'S PUZZLE ABOUT MODALITY": {
        "keywords": ["Quine", "modality", "necessary", "possible", "scope"],
        "topic": "logic"
    }
}

def get_section_for_position(content, pos_start, section_map):
    """Find the section that contains this position."""
    current_section = ""
    for start_pos, section_name in sorted(section_map.items()):
        if start_pos < pos_start:
            current_section = section_name
        else:
            break
    return current_section

def get_topic_info(section_name, topic_dict):
    """Get keywords and topic from section name."""
    for key, info in topic_dict.items():
        if key in section_name.upper():
            return info["keywords"], info["topic"]
    return ["philosophy of language"], "philosophy of language"

def extract_additional_keywords(text):
    """Extract additional keywords from position text."""
    extra_keywords = []
    important_terms = [
        "Grice", "Wittgenstein", "Russell", "Frege", "Quine", "Meinong",
        "proposition", "sentence", "meaning", "reference", "sense",
        "semantic", "syntax", "pragmatics", "truth", "false",
        "speaker", "literal", "indexical", "demonstrative",
        "quantifier", "operator", "scope", "modal", "necessary",
        "existential", "identity", "belief", "property", "instantiation",
        "substitution", "Leibniz", "compositional", "context",
        "CRS", "conceptual role", "theory of descriptions", "TD"
    ]
    text_lower = text.lower()
    for term in important_terms:
        if term.lower() in text_lower and term not in extra_keywords:
            extra_keywords.append(term)
    return extra_keywords[:5]

def parse_chapter(file_path, chapter_num, work_title, work_id, topic_dict):
    """Parse positions from a chapter file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    section_pattern = r'##\s+[IVXLCDM]+\.\s+(.+?)(?=\n)'
    section_matches = [(m.start(), m.group(1).strip()) for m in re.finditer(section_pattern, content)]
    section_map = {start: name for start, name in section_matches}
    
    position_pattern = r'\*\*(\d+)\.\*\*\s+(.+?)(?=\n\n|\n\*\*\d+\.\*\*|\n---|\n##|\Z)'
    matches = list(re.finditer(position_pattern, content, re.DOTALL))
    
    positions = []
    for match in matches:
        pos_num = int(match.group(1))
        raw_text = match.group(2).strip()
        text = re.sub(r'\s+', ' ', raw_text)
        
        section = get_section_for_position(content, match.start(), section_map)
        base_keywords, topic = get_topic_info(section, topic_dict)
        extra_keywords = extract_additional_keywords(text)
        
        all_keywords = list(set(base_keywords + extra_keywords))[:8]
        
        position = {
            "work_title": work_title,
            "work_id": work_id,
            "chapter": chapter_num,
            "section": section,
            "position_number": pos_num,
            "verbatim_quote": text,
            "thesis": text,
            "keywords": all_keywords,
            "topic_area": topic
        }
        positions.append(position)
    
    return positions

def main():
    print("Loading existing database...")
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_count = data.get("total_positions", len(data.get("positions", [])))
    print(f"Existing positions: {existing_count}")
    
    print("\nParsing Chapter 4 positions...")
    ch4_positions = parse_chapter(
        CHAPTER_4_FILE,
        4,
        "How Many Words Does It Take to Communicate a Thought? Part II: Language and Thought (Chapter 4 - What Is a Language?)",
        "kuc-hmw-ch4",
        CHAPTER_4_TOPICS
    )
    print(f"Found {len(ch4_positions)} Chapter 4 positions")
    
    print("\nParsing Chapter 6 positions...")
    ch6_positions = parse_chapter(
        CHAPTER_6_FILE,
        6,
        "How Many Words Does It Take to Communicate a Thought? Part II: Language and Thought (Chapter 6 - Russell's Improvements on Frege's Work)",
        "kuc-hmw-ch6",
        CHAPTER_6_TOPICS
    )
    print(f"Found {len(ch6_positions)} Chapter 6 positions")
    
    next_id = existing_count + 1
    new_positions = []
    
    for pos in ch4_positions:
        new_pos = {
            "id": f"kuc-{next_id:05d}",
            "position_type": "major_claim",
            "statement": pos["thesis"],
            "verbatim_quote": pos["verbatim_quote"],
            "keywords": pos["keywords"],
            "topic_area": pos["topic_area"],
            "work_title": pos["work_title"],
            "work_id": pos["work_id"],
            "position_id": f"kuc-hmw-ch4-{pos['position_number']:03d}",
            "text": pos["thesis"],
            "thesis": pos["thesis"],
            "section": pos["section"]
        }
        new_positions.append(new_pos)
        next_id += 1
    
    for pos in ch6_positions:
        new_pos = {
            "id": f"kuc-{next_id:05d}",
            "position_type": "major_claim",
            "statement": pos["thesis"],
            "verbatim_quote": pos["verbatim_quote"],
            "keywords": pos["keywords"],
            "topic_area": pos["topic_area"],
            "work_title": pos["work_title"],
            "work_id": pos["work_id"],
            "position_id": f"kuc-hmw-ch6-{pos['position_number']:03d}",
            "text": pos["thesis"],
            "thesis": pos["thesis"],
            "section": pos["section"]
        }
        new_positions.append(new_pos)
        next_id += 1
    
    data["positions"].extend(new_positions)
    data["total_positions"] = len(data["positions"])
    
    print(f"\nWriting updated database with {data['total_positions']} total positions...")
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccess! Added {len(new_positions)} new positions.")
    print(f"  - Chapter 4: {len(ch4_positions)} positions (IDs: kuc-hmw-ch4-001 to kuc-hmw-ch4-{len(ch4_positions):03d})")
    print(f"  - Chapter 6: {len(ch6_positions)} positions (IDs: kuc-hmw-ch6-001 to kuc-hmw-ch6-{len(ch6_positions):03d})")
    print(f"Total positions now: {data['total_positions']}")
    
    print("\nSample positions:")
    print(f"\nChapter 4 sample (position 1):")
    sample4 = new_positions[0]
    print(f"  ID: {sample4['id']}, position_id: {sample4['position_id']}")
    print(f"  work_id: {sample4['work_id']}")
    print(f"  keywords: {sample4['keywords']}")
    print(f"  topic: {sample4['topic_area']}")
    print(f"  section: {sample4['section']}")
    
    ch6_start = len(ch4_positions)
    print(f"\nChapter 6 sample (position 1):")
    sample6 = new_positions[ch6_start]
    print(f"  ID: {sample6['id']}, position_id: {sample6['position_id']}")
    print(f"  work_id: {sample6['work_id']}")
    print(f"  keywords: {sample6['keywords']}")
    print(f"  topic: {sample6['topic_area']}")
    print(f"  section: {sample6['section']}")

if __name__ == "__main__":
    main()
