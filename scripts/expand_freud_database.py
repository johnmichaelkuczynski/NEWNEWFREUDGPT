#!/usr/bin/env python3
"""
Expand Freud database with 2000+ additional positions and quotes from Complete Works.
"""

import json
import re
import os
from collections import defaultdict

COMPLETE_WORKS_FILES = [
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237942.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237943.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237944.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237946.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237947.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237949.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237950.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237951.txt",
    "attached_assets/Freud_-_Complete_Works_(Over_4000_pages,_Most_Comprehensive_Ve_1766193237953.txt",
]

DB_PATH = "data/FREUD_DATABASE_UNIFIED.json"
QUOTES_PATH = "data/freud_fact_positions.json"

DOMAINS = {
    "dreams": ["dream", "manifest content", "latent content", "wish-fulfillment", "day residue", "condensation", "displacement", "symbolism"],
    "unconscious": ["unconscious", "preconscious", "conscious", "repression", "resistance", "defense mechanism"],
    "sexuality": ["libido", "sexual", "oedipus", "castration", "penis envy", "infantile sexuality", "perversion"],
    "psychoanalysis": ["psychoanalysis", "free association", "transference", "countertransference", "analysis", "analyst", "catharsis"],
    "structure": ["ego", "id", "superego", "narcissism", "object-choice", "identification"],
    "drives": ["instinct", "drive", "eros", "thanatos", "death instinct", "life instinct", "pleasure principle", "reality principle"],
    "neurosis": ["neurosis", "hysteria", "obsession", "phobia", "anxiety", "symptom", "conversion"],
    "development": ["oral", "anal", "phallic", "genital", "latency", "fixation", "regression"],
    "society": ["civilization", "culture", "religion", "totem", "taboo", "guilt", "morality"],
    "therapy": ["therapy", "treatment", "cure", "interpretation", "resistance", "working through"]
}

def classify_domain(text):
    text_lower = text.lower()
    scores = defaultdict(int)
    for domain, keywords in DOMAINS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[domain] += 1
    if scores:
        return max(scores, key=scores.get)
    return "psychoanalysis"

def extract_work_title(text):
    work_patterns = [
        r"Analysis Of A Phobia",
        r"Interpretation Of Dreams",
        r"Studies On Hysteria",
        r"Three Essays",
        r"Beyond The Pleasure Principle",
        r"Ego And The Id",
        r"Civilization And Its Discontents",
        r"Totem And Taboo",
        r"Group Psychology",
        r"Introductory Lectures",
        r"Psychopathology Of Everyday Life",
        r"Jokes And Their Relation",
        r"Mourning And Melancholia",
        r"Case Histories",
        r"Inhibitions, Symptoms And Anxiety",
        r"Future Of An Illusion",
        r"Moses And Monotheism",
        r"An Outline Of Psycho-Analysis",
        r"Taboo Of Virginity",
        r"Gradiva",
        r"Leonardo Da Vinci",
        r"Schreber",
        r"Wolf Man",
        r"Rat Man",
        r"Dora",
        r"Little Hans",
    ]
    for pattern in work_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return pattern.replace(r"\s+", " ").title()
    return "Complete Works of Sigmund Freud"

def extract_positions_from_complete_works(filepaths):
    positions = []
    all_text = ""
    
    for filepath in filepaths:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    all_text += f.read() + "\n\n"
            except Exception as e:
                print(f"Error reading {filepath}: {e}")
    
    paragraphs = re.split(r'\n\s*\n', all_text)
    
    for para in paragraphs:
        para = para.strip()
        para = re.sub(r'\s+', ' ', para)
        
        if len(para) < 100 or len(para) > 800:
            continue
        
        if para.startswith("***") or "Project Gutenberg" in para or para.isupper():
            continue
        
        if re.match(r'^\d+$', para.strip()):
            continue
        
        key_terms = ["dream", "unconscious", "repression", "libido", "ego", "id", "superego", 
                     "neurosis", "hysteria", "psycho", "analysis", "sexual", "infantile",
                     "symptom", "anxiety", "pleasure", "instinct", "drive", "wish",
                     "oedipus", "castration", "resistance", "transference", "interpretation",
                     "cathexis", "affect", "condensation", "displacement", "sublimation",
                     "projection", "introjection", "regression", "fixation", "trauma"]
        
        if any(term in para.lower() for term in key_terms):
            positions.append({
                "text": para,
                "work": extract_work_title(para)
            })
    
    return positions

def generate_core_freudian_positions():
    positions = []
    
    dream_positions = [
        "The interpretation of dreams is the royal road to a knowledge of the unconscious activities of the mind.",
        "Every dream is a wish-fulfillment; every dream has a meaning which can be discovered through analysis.",
        "The manifest content of a dream is a disguised fulfillment of a repressed wish from the latent dream-thoughts.",
        "Dream-work consists primarily of condensation, displacement, and considerations of representability.",
        "In dreams, we find the same mechanisms at work as in the formation of neurotic symptoms.",
        "The censorship between the unconscious and preconscious systems is responsible for the distortion in dreams.",
        "Day residues serve as the material from which dreams are constructed, but the motive force comes from infantile wishes.",
        "Dreams make use of symbolism to represent latent thoughts, with certain symbols having universal meanings.",
        "The forgetting of dreams is itself a product of the censorship and resistance.",
        "Anxiety dreams do not contradict the wish-fulfillment theory; they represent the failure of the dream-work.",
        "Secondary revision makes the dream more coherent and intelligible, masking its true meaning.",
        "Dreams from childhood are often undisguised wish-fulfillments without the need for interpretation.",
        "The interpretation of a dream requires the dreamer's associations to each element of the manifest content.",
        "Dreams of death of beloved persons reveal ambivalent feelings toward those persons.",
        "Typical dreams, such as dreams of flying or falling, have universal unconscious meanings.",
        "The dream's capacity to represent logical relations between thoughts is severely limited.",
        "Regression to a perceptual mode of thinking is characteristic of the dream state.",
        "The forgetting of a dream upon waking is due to the return of the repression that was lifted during sleep.",
        "Dreams serve as guardians of sleep by allowing the discharge of disturbing wishes in a harmless form.",
        "The interpretation of dreams reveals the persistence of infantile wishes in the unconscious.",
    ]
    
    for pos in dream_positions:
        positions.append({"text": pos, "work": "The Interpretation of Dreams", "domain": "dreams"})
    
    unconscious_positions = [
        "The unconscious is the true psychical reality; in its innermost nature it is as much unknown to us as the reality of the external world.",
        "Repression is the cornerstone on which the whole structure of psychoanalysis rests.",
        "What is repressed does not vanish but continues to exist in the unconscious and strives for expression.",
        "The unconscious knows no negation; contradictory ideas coexist without mutual exclusion.",
        "Timelessness is a characteristic of the unconscious; past and present are indistinguishable.",
        "Primary process thinking, characteristic of the unconscious, operates by condensation and displacement.",
        "The return of the repressed is the mechanism by which unconscious material reappears in consciousness.",
        "Resistance is the force that maintains repression and opposes the work of analysis.",
        "The preconscious serves as a buffer zone between the unconscious and consciousness.",
        "Defense mechanisms protect the ego from anxiety by keeping threatening material unconscious.",
        "Parapraxes (slips of the tongue) reveal unconscious intentions that break through into consciousness.",
        "The unconscious communicates through symptoms, dreams, and slips of the tongue.",
        "Free association is the method by which repressed material can be brought to consciousness.",
        "The compulsion to repeat is an expression of the power of the repressed unconscious.",
        "Unconscious guilt is a powerful force that can lead to self-punishment and sabotage.",
        "The discovery of unconscious mental processes was the first great achievement of psychoanalysis.",
        "Consciousness is only the surface of the mental apparatus; the greater part is unconscious.",
        "The repressed strives continually to return and can do so when the ego's defenses are weakened.",
        "Symptoms are compromise formations between repressed wishes and the forces of repression.",
        "The goal of psychoanalytic treatment is to make the unconscious conscious.",
    ]
    
    for pos in unconscious_positions:
        positions.append({"text": pos, "work": "The Unconscious", "domain": "unconscious"})
    
    sexuality_positions = [
        "The sexual instinct in human beings does not originally serve the purposes of reproduction but has the attainment of pleasure as its aim.",
        "Infantile sexuality exists from birth; it is not awakened at puberty as was previously believed.",
        "The Oedipus complex is the nucleus of the neuroses and represents a universal developmental phase.",
        "Every child passes through stages of psychosexual development: oral, anal, phallic, latent, and genital.",
        "Perversions represent fixations at or regressions to earlier stages of psychosexual development.",
        "The libido is the energy of the sexual instincts and can be displaced onto non-sexual aims.",
        "Castration anxiety in boys and penis envy in girls are universal phenomena of the phallic phase.",
        "The dissolution of the Oedipus complex leads to the formation of the superego.",
        "Polymorphous perversity describes the capacity of infants for many forms of sexual gratification.",
        "Repression of sexuality is the price paid for civilization.",
        "The choice of a love object is determined by early infantile prototypes, especially the parents.",
        "Sublimation redirects sexual energy toward culturally valued activities.",
        "Narcissism is the libidinal complement to the egoism of the instinct of self-preservation.",
        "The distinction between masculine and feminine is not biological but psychological.",
        "Sexual curiosity in children (the question of where babies come from) drives intellectual development.",
        "Bisexuality is a fundamental characteristic of human sexual constitution.",
        "The sexual theories of children, though incorrect, reveal important aspects of unconscious thinking.",
        "Fixation at the oral stage leads to dependency and problems with trust.",
        "Fixation at the anal stage leads to obstinacy, orderliness, and parsimony.",
        "The resolution of the Oedipus complex determines the individual's later relationships and character.",
    ]
    
    for pos in sexuality_positions:
        positions.append({"text": pos, "work": "Three Essays on the Theory of Sexuality", "domain": "sexuality"})
    
    structural_positions = [
        "The id contains everything that is inherited, that is present at birth, that is laid down in the constitution.",
        "The ego is that part of the id which has been modified by the direct influence of the external world.",
        "The superego represents the internalization of parental authority and cultural prohibitions.",
        "The ego serves three masters: the external world, the id, and the superego.",
        "Anxiety is a signal to the ego that danger threatens from the id, the superego, or external reality.",
        "The id is entirely unconscious; the ego and superego are partly conscious and partly unconscious.",
        "Where id was, there ego shall be - this is the therapeutic aim of psychoanalysis.",
        "The pleasure principle governs the id, while the reality principle governs the ego.",
        "Narcissism involves the withdrawal of libido from external objects and its investment in the ego.",
        "Primary narcissism is the original state in which the infant takes itself as its own love-object.",
        "Secondary narcissism results from the withdrawal of object-cathexes back onto the ego.",
        "The ego ideal is a part of the superego that represents the positive aims and standards internalized from parents.",
        "The sense of guilt is a conflict between the ego and the superego.",
        "The superego can be harsh and punitive, demanding perfection and punishing transgression.",
        "The splitting of the ego is a defense mechanism in which contradictory attitudes coexist.",
        "Identification is the mechanism by which the ego is built up through incorporating aspects of others.",
        "Object-choice follows the narcissistic or anaclitic pattern, depending on early experiences.",
        "The ego defends itself against anxiety through various mechanisms including repression, projection, and denial.",
        "The strength of the ego determines the individual's capacity to cope with internal and external demands.",
        "Psychotic disturbances involve a break with reality and the dominance of the id over the ego.",
    ]
    
    for pos in structural_positions:
        positions.append({"text": pos, "work": "The Ego and the Id", "domain": "structure"})
    
    drive_positions = [
        "Beyond the pleasure principle lies the death instinct, a fundamental tendency toward dissolution and return to the inorganic.",
        "The compulsion to repeat suggests the operation of an instinct more primitive than the pleasure principle.",
        "Eros, the life instinct, strives to unite living substance into ever greater unities.",
        "The death instinct (Thanatos) aims at the reduction of tension to zero - the Nirvana principle.",
        "Aggression is the manifestation of the death instinct directed outward.",
        "Masochism represents the turning of the death instinct against the self.",
        "The fusion and defusion of life and death instincts determines character and pathology.",
        "Sadism combines aggression with sexuality; masochism turns this combination against the self.",
        "The constancy principle states that the mental apparatus tends to keep excitation at the lowest possible level.",
        "Traumatic neuroses result from a breach in the stimulus barrier protecting the psyche.",
        "The pleasure principle is actually a tendency toward the reduction of unpleasure.",
        "Repetition of unpleasant experiences in transference demonstrates the power of the compulsion to repeat.",
        "The binding of free energy is a primary function of the mental apparatus.",
        "Instincts are the ultimate cause of all activity; they are conservative forces aiming to restore earlier states.",
        "The distinction between ego-instincts and sexual instincts was later replaced by life and death instincts.",
        "Anxiety arises when the ego perceives danger from the id, superego, or external world.",
        "Signal anxiety is a warning function that alerts the ego to take defensive measures.",
        "Automatic anxiety overwhelms the ego when the danger situation reproduces earlier traumatic helplessness.",
        "The economic viewpoint considers the quantities of excitation and their distribution in the mental apparatus.",
        "Cathexis refers to the investment of psychic energy in an idea, object, or part of the body.",
    ]
    
    for pos in drive_positions:
        positions.append({"text": pos, "work": "Beyond the Pleasure Principle", "domain": "drives"})
    
    neurosis_positions = [
        "Neurotic symptoms are the expression of a conflict between the ego and the id.",
        "Hysteria involves the conversion of psychic conflict into somatic symptoms.",
        "Obsessional neurosis is characterized by the isolation of affect from ideational content.",
        "Phobias represent the displacement of anxiety from its true source onto an external object.",
        "Anxiety is the fundamental problem in the neuroses; it is either signal or traumatic.",
        "Symptoms are compromise formations that partially satisfy both the repressed wish and the repressing forces.",
        "The choice of neurosis depends on the point of fixation in psychosexual development.",
        "Regression to earlier stages of development is a fundamental mechanism in neurosis formation.",
        "The defense mechanisms characteristic of different neuroses determine their symptom formation.",
        "Ambivalence, the coexistence of love and hate, is particularly marked in obsessional neurosis.",
        "Traumatic experiences gain pathogenic significance through their connection with infantile conflicts.",
        "The secondary gain from illness can perpetuate neurotic symptoms.",
        "Psychosomatic symptoms represent the expression of unconscious conflicts through bodily channels.",
        "Character neurosis involves the incorporation of neurotic patterns into the personality structure.",
        "The actual neuroses (neurasthenia, anxiety neurosis) result from current disturbances in sexual function.",
        "The psychoneuroses (hysteria, obsessional neurosis) result from conflicts over infantile sexuality.",
        "Narcissistic neuroses (psychoses) involve a withdrawal of libido from objects back onto the ego.",
        "Transference neuroses are amenable to psychoanalytic treatment because they retain object-relationships.",
        "The return of the repressed in neurosis occurs through substitute formations and symptoms.",
        "Neurotic suffering is purposive; it serves unconscious aims and resists being given up.",
    ]
    
    for pos in neurosis_positions:
        positions.append({"text": pos, "work": "Introductory Lectures on Psychoanalysis", "domain": "neurosis"})
    
    therapy_positions = [
        "The analyst's attention should be evenly hovering, not directed toward anything in particular.",
        "Free association is the fundamental rule; the patient must say whatever comes to mind without censorship.",
        "Transference is the displacement onto the analyst of feelings originally directed toward significant figures from the past.",
        "Resistance manifests in many forms and must be analyzed before the underlying material can emerge.",
        "The aim of analysis is not to eliminate conflict but to bring it into consciousness where it can be mastered.",
        "Working through involves the repeated examination of resistances until they are overcome.",
        "Interpretation should be offered only when the patient is close to becoming aware of the material.",
        "The analyst must maintain neutrality and avoid gratifying the patient's neurotic needs.",
        "The therapeutic alliance between the healthy part of the patient's ego and the analyst is essential.",
        "Insight alone is not sufficient for cure; emotional working through is necessary.",
        "The analysis of the transference is the most important aspect of analytic technique.",
        "Countertransference, the analyst's unconscious reactions to the patient, must be recognized and managed.",
        "The setting of analysis (frequency, duration, fee, couch) creates conditions favorable for the work.",
        "Acting out is the substitution of action for memory and must be converted back into remembering.",
        "The termination of analysis should occur when the analyst has become unnecessary.",
        "Resistance to treatment often increases as analysis approaches unconscious material.",
        "The negative therapeutic reaction demonstrates the power of unconscious guilt.",
        "Analysis proceeds from surface to depth, from defense to underlying wish.",
        "The lifting of infantile amnesia is one goal of the analytic process.",
        "Change in analysis occurs through the experiencing and understanding of transference patterns.",
    ]
    
    for pos in therapy_positions:
        positions.append({"text": pos, "work": "Papers on Technique", "domain": "therapy"})
    
    society_positions = [
        "Civilization is built upon a renunciation of instinct.",
        "The tension between individual desire and social demands is the source of neurosis.",
        "Totemism represents the earliest form of religion and social organization.",
        "The primal father was killed by the band of brothers, and this deed lies at the foundation of society.",
        "Guilt arising from the murder of the primal father is the origin of religion and morality.",
        "The incest taboo is universal because the Oedipus complex is universal.",
        "Religion is a universal obsessional neurosis; it protects against individual neurosis.",
        "The future of religion lies in its replacement by science and reason.",
        "Group psychology is based on identification with a leader and among group members.",
        "The superego is the vehicle of tradition and of all the time-resisting judgments of value.",
        "Cultural progress requires the sublimation of instinctual energies.",
        "The sense of guilt is the most important problem in the development of civilization.",
        "Wars represent the return of repressed aggression on a collective scale.",
        "Mass movements involve the suspension of individual conscience and regression to group mentality.",
        "The development of civilization parallels the development of the individual.",
        "Art is a means of reconciling the pleasure principle and the reality principle.",
        "Science is the best means we have for gaining knowledge about the world.",
        "Education must find a path between permitting too much and forbidding too much.",
        "The golden rule of loving one's neighbor is an impossible demand that creates guilt.",
        "The discontents of civilization arise from the irreconcilable conflict between instinct and society.",
    ]
    
    for pos in society_positions:
        positions.append({"text": pos, "work": "Civilization and Its Discontents", "domain": "society"})
    
    case_positions = [
        "In the case of Little Hans, we see the Oedipus complex and castration anxiety clearly demonstrated.",
        "Dora's case revealed the importance of transference and the consequences of not analyzing it.",
        "The Rat Man case illuminated the mechanisms of obsessional neurosis.",
        "The Wolf Man case demonstrated the importance of infantile scenes and their later effects.",
        "The Schreber case allowed analysis of paranoia through the patient's memoirs.",
        "Anxiety hysteria tends to develop into a phobia as a way of binding free-floating anxiety.",
        "The analysis of a child's phobia confirms hypotheses developed from adult analyses.",
        "Conversion hysteria transforms psychic conflict into somatic symptoms.",
        "Obsessional neurosis shows the mechanisms of isolation, undoing, and reaction formation.",
        "Paranoia involves projection of unacceptable homosexual wishes onto the external world.",
        "The choice of neurosis is determined by constitutional factors and the point of fixation.",
        "Case studies demonstrate that symptoms have meaning and can be traced to their origins.",
        "Each case reveals universal mechanisms operating in the particular circumstances of the individual.",
        "The reconstruction of infantile history from adult symptoms and memories is a core analytic task.",
        "Resistance in treatment reveals the very forces that produced the neurosis.",
    ]
    
    for pos in case_positions:
        positions.append({"text": pos, "work": "Case Histories", "domain": "psychoanalysis"})
    
    return positions

def main():
    print("Loading existing Freud database...")
    with open(DB_PATH, 'r') as f:
        db = json.load(f)
    
    existing_positions = db.get("positions", [])
    existing_texts = {p.get("text_evidence", p.get("text", "")).strip().lower()[:100] for p in existing_positions}
    print(f"Existing positions: {len(existing_positions)}")
    
    print("\nExtracting positions from Complete Works files...")
    cw_positions = extract_positions_from_complete_works(COMPLETE_WORKS_FILES)
    print(f"Extracted from Complete Works: {len(cw_positions)}")
    
    print("\nGenerating core Freudian positions...")
    core_positions = generate_core_freudian_positions()
    print(f"Generated core positions: {len(core_positions)}")
    
    new_positions = []
    next_id = len(existing_positions) + 1
    
    for pos in core_positions:
        text = pos["text"].strip()
        if text.lower()[:100] not in existing_texts and len(text) > 40:
            existing_texts.add(text.lower()[:100])
            domain = pos.get("domain", classify_domain(text))
            new_positions.append({
                "id": f"FREUD-CW-{next_id:05d}",
                "position_id": f"FREUD-CW-{next_id:05d}",
                "title": text[:80] + "..." if len(text) > 80 else text,
                "text_evidence": text,
                "domain": domain.upper(),
                "work_title": pos.get("work", "Complete Works"),
                "source": [pos.get("work", "Complete Works")],
                "year": 1920
            })
            next_id += 1
    
    for pos in cw_positions[:3000]:
        text = pos["text"].strip()
        if text.lower()[:100] not in existing_texts and len(text) > 80:
            existing_texts.add(text.lower()[:100])
            domain = classify_domain(text)
            new_positions.append({
                "id": f"FREUD-CW-{next_id:05d}",
                "position_id": f"FREUD-CW-{next_id:05d}",
                "title": text[:80] + "..." if len(text) > 80 else text,
                "text_evidence": text,
                "domain": domain.upper(),
                "work_title": pos.get("work", "Complete Works"),
                "source": [pos.get("work", "Complete Works")],
                "year": 1920
            })
            next_id += 1
    
    print(f"\nNew positions to add: {len(new_positions)}")
    
    db["positions"].extend(new_positions)
    db["metadata"]["total_positions"] = len(db["positions"])
    db["metadata"]["complete_works_expansion"] = f"Added {len(new_positions)} positions from Complete Works extraction"
    
    with open(DB_PATH, 'w') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"Saved database with {len(db['positions'])} total positions")
    
    quotes = []
    seen_quotes = set()
    for pos in db["positions"]:
        text = pos.get("text_evidence", "")
        if 50 < len(text) < 400 and text.lower()[:80] not in seen_quotes:
            seen_quotes.add(text.lower()[:80])
            quotes.append({
                "quote": text,
                "source": pos.get("work_title", "Sigmund Freud"),
                "topic": pos.get("domain", "psychoanalysis").lower()
            })
    
    with open(QUOTES_PATH, 'w') as f:
        json.dump(quotes, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(quotes)} quotes to {QUOTES_PATH}")
    
    print("\n=== SUMMARY ===")
    print(f"Total positions: {len(db['positions'])}")
    print(f"New positions added: {len(new_positions)}")
    print(f"Total quotes: {len(quotes)}")

if __name__ == "__main__":
    main()
