#!/usr/bin/env python3
"""
Add Chapter 5 (Analytic Philosophy - Language and Thought) positions to Kuczynski database.
150 positions covering: Do we think in language? Private language argument, mental imagery, etc.
"""

import json

CHAPTER5_POSITIONS = [
    {"thesis": "[Ch5] It is obvious that knowledge of a language makes one more intelligent in at least some respects.", "keywords": ["language", "intelligence", "knowledge", "cognition"]},
    {"thesis": "[Ch5] Knowledge of a language makes one more intelligent in at least some respects.", "keywords": ["language", "intelligence", "cognition"]},
    {"thesis": "[Ch5] Authoritarian governments tend to be less responsive to the needs of their constituents than democratic governments.", "keywords": ["government", "authoritarianism", "democracy", "politics"]},
    {"thesis": "[Ch5] One could not grasp that thought without knowing some language or other.", "keywords": ["thought", "language", "abstraction", "cognition"]},
    {"thesis": "[Ch5] We have at least some inclination to say that one could not grasp that thought without knowing some language.", "keywords": ["thought", "language", "intuition"]},
    {"thesis": "[Ch5] We are reluctant to regard creatures that cannot interact with reality through a language as capable of grasping abstract principles.", "keywords": ["language", "abstraction", "cognition", "animals"]},
    {"thesis": "[Ch5] We are reluctant to regard language-less creatures as capable of thinking about reality in a discursive manner.", "keywords": ["language", "discursive thought", "cognition"]},
    {"thesis": "[Ch5] Whatever one can grasp through language, one must be able to grasp independently of language.", "keywords": ["language", "thought", "independence", "grasp"]},
    {"thesis": "[Ch5] This view (that thought is independent of language) is counterintuitive.", "keywords": ["thought", "language", "intuition", "counterintuitive"]},
    {"thesis": "[Ch5] Our untutored intuitions incline us to hold that without knowledge of a language a creature would be incapable of thinking discursively.", "keywords": ["intuition", "language", "discursive thought"]},
    {"thesis": "[Ch5] Untutored intuitions are not always probative.", "keywords": ["intuition", "methodology", "epistemology"]},
    {"thesis": "[Ch5] Sometimes untutored intuitions are inconsistent with one another.", "keywords": ["intuition", "inconsistency", "methodology"]},
    {"thesis": "[Ch5] We strongly feel that we sometimes have thoughts of considerable sophistication that we don't know how to put into words.", "keywords": ["thought", "language", "inexpressibility", "sophistication"]},
    {"thesis": "[Ch5] Not all discursive thought is language-dependent.", "keywords": ["discursive thought", "language", "independence"]},
    {"thesis": "[Ch5] The purpose of the chapter is to answer the question: Do we think in language?", "keywords": ["thought", "language", "methodology", "chapter thesis"]},
    {"thesis": "[Ch5] We do not think in language.", "keywords": ["thought", "language", "main thesis"]},
    {"thesis": "[Ch5] There are two very different versions of the view that we think in language.", "keywords": ["thought", "language", "versions", "theory"]},
    {"thesis": "[Ch5] Version #1: People think in the natural languages that they learn (English speakers in English, etc.).", "keywords": ["natural language", "thought", "version 1"]},
    {"thesis": "[Ch5] A natural language is one that organically arises through human interactions.", "keywords": ["natural language", "definition", "origin"]},
    {"thesis": "[Ch5] Artificial languages are invented (e.g., by programmers or philosophers).", "keywords": ["artificial language", "definition", "invention"]},
    {"thesis": "[Ch5] Version #2: We think in an innately known code, a 'language of thought.'", "keywords": ["language of thought", "innate", "Fodor", "version 2"]},
    {"thesis": "[Ch5] In Version #2, the sentences of thought belong to a hard-wired system of symbolism.", "keywords": ["language of thought", "hard-wired", "symbolism"]},
    {"thesis": "[Ch5] Version #1 is wrong.", "keywords": ["natural language", "thought", "refutation"]},
    {"thesis": "[Ch5] We can have thoughts that we are incapable of putting into words.", "keywords": ["thought", "inexpressibility", "language limits"]},
    {"thesis": "[Ch5] We grasp those thoughts in some way other than by grasping the sentences that express them.", "keywords": ["thought", "grasp", "non-linguistic"]},
    {"thesis": "[Ch5] There are occasions where putting a thought into words requires great effort.", "keywords": ["thought", "expression", "effort", "articulation"]},
    {"thesis": "[Ch5] Thinking is often a prerequisite to using language.", "keywords": ["thinking", "language", "prerequisite", "priority"]},
    {"thesis": "[Ch5] At least some thinking is non-linguistic.", "keywords": ["thinking", "non-linguistic", "cognition"]},
    {"thesis": "[Ch5] Many authors (e.g., Wittgenstein, Blackburn, McDowell) deny that we know anything that we can't readily articulate.", "keywords": ["Wittgenstein", "knowledge", "articulation", "expressibility"]},
    {"thesis": "[Ch5] 'If you can't say it, you don't know it.'", "keywords": ["knowledge", "expression", "slogan", "criticism"]},
    {"thesis": "[Ch5] A person's beliefs can be expressed in many ways, not all linguistic.", "keywords": ["belief", "expression", "non-linguistic"]},
    {"thesis": "[Ch5] Knowledge can be expressed in drawings, movements, or other non-linguistic manners.", "keywords": ["knowledge", "expression", "drawing", "non-linguistic"]},
    {"thesis": "[Ch5] Accurate painting involves bona fide knowledge, not pseudo-knowledge.", "keywords": ["painting", "knowledge", "art", "genuine"]},
    {"thesis": "[Ch5] Some kinds of information (e.g., visual) seem inherently incapable of being fully expressed by sentences of natural languages.", "keywords": ["visual information", "inexpressibility", "limits of language"]},
    {"thesis": "[Ch5] Sentences have very different structures from pictures.", "keywords": ["sentences", "pictures", "structure", "difference"]},
    {"thesis": "[Ch5] Sentences are digital structures (decompose into discrete parts).", "keywords": ["sentences", "digital", "discrete", "structure"]},
    {"thesis": "[Ch5] Sense-perceptions are analogue structures (do not decompose into discrete parts).", "keywords": ["perception", "analogue", "continuous", "structure"]},
    {"thesis": "[Ch5] Any sentence must be interpreted to be understood.", "keywords": ["sentence", "interpretation", "understanding"]},
    {"thesis": "[Ch5] Perceptions are self-interpreting in a way that sentences are not.", "keywords": ["perception", "self-interpreting", "sentences", "contrast"]},
    {"thesis": "[Ch5] In order to learn a language, one must already be able to think.", "keywords": ["language learning", "thought", "prerequisite", "priority"]},
    {"thesis": "[Ch5] Learning a language presupposes the ability to synthesize information and make judgments.", "keywords": ["language learning", "synthesis", "judgment", "prerequisite"]},
    {"thesis": "[Ch5] Knowledge of a language presupposes the ability to think.", "keywords": ["language knowledge", "thought", "prerequisite"]},
    {"thesis": "[Ch5] Different sentences can have the same meaning.", "keywords": ["synonymy", "meaning", "sentences"]},
    {"thesis": "[Ch5] A single sentence can have multiple meanings.", "keywords": ["ambiguity", "meaning", "sentences"]},
    {"thesis": "[Ch5] 'Bob loves Mary' and 'Mary is loved by Bob' have the same meaning but are different sentences.", "keywords": ["synonymy", "example", "active voice", "passive voice"]},
    {"thesis": "[Ch5] If we thought in sentences, those would constitute different beliefs, but they do not.", "keywords": ["thought", "sentences", "belief", "identity"]},
    {"thesis": "[Ch5] We can disambiguate ambiguous sentences, which would be impossible if thoughts were identical with sentence-occurrences.", "keywords": ["disambiguation", "thought", "sentence", "identity"]},
    {"thesis": "[Ch5] People who speak different languages can have the same thoughts.", "keywords": ["translation", "thought", "language independence"]},
    {"thesis": "[Ch5] Understanding sentences involves thought.", "keywords": ["understanding", "sentences", "thought"]},
    {"thesis": "[Ch5] Understanding a sentence is different from its flashing through your mind.", "keywords": ["understanding", "mental occurrence", "distinction"]},
    {"thesis": "[Ch5] Version #2 (language of thought) is false.", "keywords": ["language of thought", "Fodor", "refutation"]},
    {"thesis": "[Ch5] We often think in images (visual and auditory).", "keywords": ["mental imagery", "thinking", "visual", "auditory"]},
    {"thesis": "[Ch5] Images have a structure fundamentally different from sentences.", "keywords": ["images", "sentences", "structure", "difference"]},
    {"thesis": "[Ch5] Knowing a language involves understanding its expressions and their semantic rules.", "keywords": ["language knowledge", "understanding", "semantic rules"]},
    {"thesis": "[Ch5] It is viciously circular to hold that thought depends on an innate code whose rules must be understood.", "keywords": ["circularity", "language of thought", "understanding", "vicious circle"]},
    {"thesis": "[Ch5] Advocates say we don't understand the innate sentences; we are merely built to conform to them.", "keywords": ["language of thought", "conformity", "understanding", "objection"]},
    {"thesis": "[Ch5] If sentences aren't understood, they aren't functioning as sentences.", "keywords": ["sentences", "understanding", "function"]},
    {"thesis": "[Ch5] We don't think in language, even an innate one.", "keywords": ["thought", "language", "innate", "main thesis"]},
    {"thesis": "[Ch5] Mental images (icons) on a computer desktop represent changes in electrical activity.", "keywords": ["icons", "representation", "computer", "analogy"]},
    {"thesis": "[Ch5] Thoughts often take the form of a voice or mental images of spoken words.", "keywords": ["inner speech", "mental imagery", "thought form"]},
    {"thesis": "[Ch5] People think with the help of visual imagery.", "keywords": ["visual imagery", "thinking", "aid"]},
    {"thesis": "[Ch5] Mental images are not identical with the ratiocinative activities they facilitate.", "keywords": ["mental images", "ratiocination", "facilitation", "identity"]},
    {"thesis": "[Ch5] Images need only be sufficiently differentiated to avoid confusion.", "keywords": ["images", "differentiation", "function"]},
    {"thesis": "[Ch5] Ratiocinative activity cannot be identical with any sequence of images.", "keywords": ["ratiocination", "images", "identity", "impossibility"]},
    {"thesis": "[Ch5] Everything constitutive of consciousness seems image-like or phenomenologically pregnant.", "keywords": ["consciousness", "imagery", "phenomenology"]},
    {"thesis": "[Ch5] Wittgenstein concluded that thinking isn't a private psychological act.", "keywords": ["Wittgenstein", "thinking", "private", "psychological"]},
    {"thesis": "[Ch5] Thinking consists of engaging in overt behaviors involving public language symbols.", "keywords": ["Wittgenstein", "thinking", "behavior", "public language"]},
    {"thesis": "[Ch5] Wittgenstein's position is absurd.", "keywords": ["Wittgenstein", "criticism", "absurdity"]},
    {"thesis": "[Ch5] Thoughts, unlike itches and tickles, aren't phenomenologically pregnant.", "keywords": ["thoughts", "phenomenology", "sensation", "contrast"]},
    {"thesis": "[Ch5] Wittgenstein's mistake is similar to Hume's on personal identity.", "keywords": ["Wittgenstein", "Hume", "personal identity", "analogy"]},
    {"thesis": "[Ch5] Thinking is a psychological process.", "keywords": ["thinking", "psychology", "process"]},
    {"thesis": "[Ch5] Mental imagery facilitates thought.", "keywords": ["mental imagery", "thought", "facilitation"]},
    {"thesis": "[Ch5] Mental images allow us to manage thought-processes that we otherwise couldn't manage.", "keywords": ["mental images", "thought management", "cognition"]},
    {"thesis": "[Ch5] Consciousness integrates otherwise isolated streams of cognitive activity.", "keywords": ["consciousness", "integration", "cognition", "unity"]},
    {"thesis": "[Ch5] Knowledge of a language provides a rich system of icons for managing cognitive activities.", "keywords": ["language", "icons", "cognitive management"]},
    {"thesis": "[Ch5] Wittgenstein contended that there cannot be a private language.", "keywords": ["Wittgenstein", "private language", "impossibility"]},
    {"thesis": "[Ch5] Private codes must be translations of public languages.", "keywords": ["private code", "public language", "translation"]},
    {"thesis": "[Ch5] A single person can use a public language privately, but it's parasitic on public use.", "keywords": ["private use", "public language", "parasitism"]},
    {"thesis": "[Ch5] It is logically impossible for a solitary individual to create a language.", "keywords": ["Wittgenstein", "solitary language", "impossibility"]},
    {"thesis": "[Ch5] One cannot think unless one knows a language.", "keywords": ["thought", "language", "prerequisite", "Wittgenstein"]},
    {"thesis": "[Ch5] Knowledge of a language is prerequisite for reasoning.", "keywords": ["language", "reasoning", "prerequisite"]},
    {"thesis": "[Ch5] Thinking requires being embedded in a society.", "keywords": ["thinking", "society", "embeddedness", "Wittgenstein"]},
    {"thesis": "[Ch5] Wittgenstein's Private Language Argument (PLA) argues there cannot be private languages.", "keywords": ["private language argument", "Wittgenstein", "PLA"]},
    {"thesis": "[Ch5] Rule-following arguments show one cannot think without language.", "keywords": ["rule-following", "thought", "language", "Wittgenstein"]},
    {"thesis": "[Ch5] Not all ideation is ratiocinative.", "keywords": ["ideation", "ratiocination", "distinction"]},
    {"thesis": "[Ch5] Ratiocinative ideation must be rule-governed.", "keywords": ["ratiocination", "rules", "governance"]},
    {"thesis": "[Ch5] Thinking involves following rules.", "keywords": ["thinking", "rules", "rule-following"]},
    {"thesis": "[Ch5] There is no psychological condition that necessarily accompanies rule-following.", "keywords": ["rule-following", "psychology", "accompaniment"]},
    {"thesis": "[Ch5] Following a rule is not a psychological act.", "keywords": ["rule-following", "psychology", "Wittgenstein"]},
    {"thesis": "[Ch5] Not all mental states are images or sensations.", "keywords": ["mental states", "images", "sensations", "variety"]},
    {"thesis": "[Ch5] Beliefs are stable, enduring structures, not fleeting events.", "keywords": ["beliefs", "stability", "structure", "events"]},
    {"thesis": "[Ch5] Meanings are themselves symbols.", "keywords": ["meanings", "symbols", "regress"]},
    {"thesis": "[Ch5] Positing meanings to explain symbol-comprehension is circular (like the homunculus fallacy).", "keywords": ["meanings", "circularity", "homunculus", "fallacy"]},
    {"thesis": "[Ch5] Wittgenstein's argument resembles Aristotle's Third Man Argument.", "keywords": ["Wittgenstein", "Aristotle", "Third Man", "analogy"]},
    {"thesis": "[Ch5] Properties are not instances of themselves.", "keywords": ["properties", "self-instantiation", "logic"]},
    {"thesis": "[Ch5] Meanings are not themselves understood or interpreted.", "keywords": ["meanings", "understanding", "interpretation"]},
    {"thesis": "[Ch5] Meanings are grasped or not grasped.", "keywords": ["meanings", "grasp", "binary"]},
    {"thesis": "[Ch5] There is no gap between grasping a meaning and applying it (to the extent grasp is determinative).", "keywords": ["meaning", "grasp", "application", "gap"]},
    {"thesis": "[Ch5] Principles aren't interpreted; they're grasped and guide judgments.", "keywords": ["principles", "interpretation", "grasp", "judgment"]},
    {"thesis": "[Ch5] The Private Language Argument imagines a solitary person creating a language.", "keywords": ["private language argument", "solitary", "thought experiment"]},
    {"thesis": "[Ch5] In a private language, expressions mean whatever the person thinks they mean.", "keywords": ["private language", "meaning", "subjective"]},
    {"thesis": "[Ch5] A symbol that can't be used wrongly doesn't mean anything.", "keywords": ["symbol", "correctness", "meaning", "normativity"]},
    {"thesis": "[Ch5] Languages require right and wrong ways of use, which require multiple people.", "keywords": ["language", "normativity", "community", "Wittgenstein"]},
    {"thesis": "[Ch5] All languages are public.", "keywords": ["language", "public", "Wittgenstein thesis"]},
    {"thesis": "[Ch5] The Private Language Argument is spurious.", "keywords": ["private language argument", "criticism", "refutation"]},
    {"thesis": "[Ch5] Expressions are meaningful because people remember what they mean.", "keywords": ["meaning", "memory", "correctness"]},
    {"thesis": "[Ch5] Forgetting semantic rules renders a language useless to the individual.", "keywords": ["memory", "semantic rules", "usefulness"]},
    {"thesis": "[Ch5] If a person changes meanings, they create a new language.", "keywords": ["meaning change", "new language", "identity"]},
    {"thesis": "[Ch5] Thinking involves following rules.", "keywords": ["thinking", "rules", "rule-following"]},
    {"thesis": "[Ch5] Rule-following is a psychological act.", "keywords": ["rule-following", "psychology", "against Wittgenstein"]},
    {"thesis": "[Ch5] Thought is a psychological act.", "keywords": ["thought", "psychology", "act"]},
    {"thesis": "[Ch5] A prerequisite for speaking a language is knowing its semantic rules.", "keywords": ["speaking", "semantic rules", "prerequisite"]},
    {"thesis": "[Ch5] Thought mediates meaningful use of language.", "keywords": ["thought", "meaning", "language", "mediation"]},
    {"thesis": "[Ch5] Wittgenstein's arguments for his conclusions are not probative.", "keywords": ["Wittgenstein", "arguments", "criticism", "non-probative"]},
    {"thesis": "[Ch5] We have no good reason to accept Wittgenstein's position that thought consists in manipulating public symbols.", "keywords": ["Wittgenstein", "thought", "public symbols", "rejection"]},
    {"thesis": "[Ch5] We know Wittgenstein's position to be erroneous.", "keywords": ["Wittgenstein", "error", "refutation"]},
    {"thesis": "[Ch5] Not all thought involves the use of a public language.", "keywords": ["thought", "public language", "independence"]},
    {"thesis": "[Ch5] We don't think in an innate language or code.", "keywords": ["thought", "innate language", "language of thought", "rejection"]},
    {"thesis": "[Ch5] Some kinds of cognition necessarily involve language, others don't.", "keywords": ["cognition", "language", "variety", "dependence"]},
    {"thesis": "[Ch5] Wittgenstein held there cannot be a private language.", "keywords": ["Wittgenstein", "private language", "position"]},
    {"thesis": "[Ch5] Wittgenstein held one cannot think without knowing a language.", "keywords": ["Wittgenstein", "thought", "language", "position"]},
    {"thesis": "[Ch5] Meanings don't have to be interpreted.", "keywords": ["meanings", "interpretation", "directness"]},
    {"thesis": "[Ch5] Visual perceptions are analogue, sentences are digital.", "keywords": ["perception", "analogue", "sentences", "digital"]},
    {"thesis": "[Ch5] Learning language requires prior thought.", "keywords": ["language learning", "thought", "priority"]},
    {"thesis": "[Ch5] Same thoughts can be expressed in different languages.", "keywords": ["thought", "translation", "language independence"]},
    {"thesis": "[Ch5] Mental imagery is not constitutive of thought but facilitates it.", "keywords": ["mental imagery", "thought", "facilitation", "constitution"]},
    {"thesis": "[Ch5] Consciousness pools otherwise discrete bodies of knowledge.", "keywords": ["consciousness", "integration", "knowledge", "unity"]},
    {"thesis": "[Ch5] Language provides icons for cognitive management.", "keywords": ["language", "icons", "cognitive management"]},
    {"thesis": "[Ch5] Rule-following is a psychological act.", "keywords": ["rule-following", "psychology", "against Wittgenstein"]},
    {"thesis": "[Ch5] Beliefs are not phenomenologically pregnant.", "keywords": ["beliefs", "phenomenology", "non-phenomenal"]},
    {"thesis": "[Ch5] Thinking is private and psychological.", "keywords": ["thinking", "private", "psychological"]},
    {"thesis": "[Ch5] Private languages are possible.", "keywords": ["private language", "possibility", "against Wittgenstein"]},
    {"thesis": "[Ch5] Solitary individuals can think.", "keywords": ["solitary", "thought", "possibility"]},
    {"thesis": "[Ch5] Meanings are grasped directly, not interpreted.", "keywords": ["meanings", "direct grasp", "interpretation"]},
    {"thesis": "[Ch5] Semantic rules determine meaning independently of ongoing interpretation.", "keywords": ["semantic rules", "meaning", "interpretation", "independence"]},
    {"thesis": "[Ch5] Understanding a sentence requires more than mere imagery of it.", "keywords": ["understanding", "sentence", "imagery", "distinction"]},
    {"thesis": "[Ch5] Thoughts precede and enable language acquisition.", "keywords": ["thought", "language acquisition", "priority"]},
    {"thesis": "[Ch5] Ambiguous sentences can be disambiguated non-linguistically.", "keywords": ["ambiguity", "disambiguation", "non-linguistic"]},
    {"thesis": "[Ch5] Non-linguistic expression of knowledge is possible (e.g., drawing).", "keywords": ["knowledge", "expression", "non-linguistic", "drawing"]},
    {"thesis": "[Ch5] Visual information cannot be fully captured linguistically.", "keywords": ["visual information", "language limits", "inexpressibility"]},
    {"thesis": "[Ch5] Perceptions do not require interpretation like sentences do.", "keywords": ["perception", "interpretation", "sentences", "contrast"]},
    {"thesis": "[Ch5] Knowledge of language enhances cognition by providing manipulable icons.", "keywords": ["language", "cognition", "icons", "enhancement"]},
    {"thesis": "[Ch5] Mental images serve as surrogates for concepts.", "keywords": ["mental images", "concepts", "surrogacy"]},
    {"thesis": "[Ch5] Wittgenstein wrongly infers thought is public behavior.", "keywords": ["Wittgenstein", "thought", "behavior", "error"]},
    {"thesis": "[Ch5] Wittgenstein's rule-following arguments fail because they assume all mental states are phenomenal.", "keywords": ["Wittgenstein", "rule-following", "phenomenal", "criticism"]},
    {"thesis": "[Ch5] The private language argument fails because memory provides objective standards for correctness.", "keywords": ["private language argument", "memory", "objectivity", "refutation"]},
    {"thesis": "[Ch5] Changing intended meanings creates a new language, not arbitrary meaning in the old one.", "keywords": ["meaning change", "new language", "identity"]},
    {"thesis": "[Ch5] Public languages are causally entrenched but not logically different from private ones.", "keywords": ["public language", "private language", "causal", "logical"]},
    {"thesis": "[Ch5] Thought is independent of public language.", "keywords": ["thought", "public language", "independence"]},
    {"thesis": "[Ch5] We do not think in words, whether public or innate.", "keywords": ["thought", "words", "language", "main conclusion"]},
]

WORK_TITLE = "How Many Words (Chapter 5: Analytic Philosophy - Language and Thought)"

def main():
    with open('data/KUCZYNSKI_COMPREHENSIVE_DATABASE.json', 'r') as f:
        data = json.load(f)
    
    initial_count = len(data['positions'])
    print(f"Initial position count: {initial_count}")
    
    new_positions = []
    for pos in CHAPTER5_POSITIONS:
        new_positions.append({
            "work_title": WORK_TITLE,
            "thesis": pos["thesis"],
            "keywords": pos["keywords"]
        })
    
    data['positions'].extend(new_positions)
    data['total_positions'] = len(data['positions'])
    
    with open('data/KUCZYNSKI_COMPREHENSIVE_DATABASE.json', 'w') as f:
        json.dump(data, f, indent=2)
    
    final_count = len(data['positions'])
    print(f"Added {final_count - initial_count} Chapter 5 positions")
    print(f"Final position count: {final_count}")
    print(f"Total positions field: {data['total_positions']}")

if __name__ == "__main__":
    main()
