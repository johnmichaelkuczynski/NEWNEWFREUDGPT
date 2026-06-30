#!/usr/bin/env python3
"""
Add Analytic Philosophy Chapter 18 positions with quotes to the Kuczynski database.
Topics: Modal Logic, Necessity, Analyticity, Kripke, Quine
"""

import json
from datetime import datetime

ch18_positions = [
    ("Modal statements describe what could or must be the case.", "Modal Logic", "A modal statement is one that says what could be the case or what must be the case."),
    ("Necessity and possibility are logical relations between propositions.", "Modal Logic", "For any proposition P, it's necessarily the case that P iff it's not possible that not-P."),
    ("There are no impossible objects.", "Modal Logic", "There are no impossible objects—no objects that couldn't possibly exist."),
    ("Possibility is a property of propositions, not objects.", "Modal Logic", "Possibility and impossibility are properties of propositions, not of objects."),
    ("Statements of non-existence are about propositions, not objects.", "Logic", "Statements that, given their surface-structures, appear to attribute non-existence to objects in fact attribute falsity to propositions."),
    ("Fictional characters are false existence claims.", "Logic", "The cartoons that brought Fred Flintstone and Bart Simpson into our homes can be thought of as making false statements."),
    ("Necessity does not come in degrees.", "Modal Logic", "There are only two degrees of necessity: having it completely and lacking it completely."),
    ("Highly necessary statements hold in more circumstances.", "Modal Logic", "Some statements need less help from others to be true—those are the 'highly necessary' ones."),
    ("Kripke argued for non-analytic necessary truths.", "Modal Logic", "In 1969, Saul Kripke gave a now famous series of lectures in which he argued that there are non-analytic necessary truths."),
    ("Proper names are rigid designators.", "Modal Logic", "In general, proper names are rigid designators."),
    ("'Hesperus is Phosphorus' expresses a necessary truth.", "Modal Logic", "'Hesperus is Phosphorous' expresses a non-analytic necessary truth."),
    ("Kripke's argument confuses semantics with pre-semantics.", "Modal Logic", "In each case, semantics is being confused with pre-semantics."),
    ("Modal concepts reduce to necessity.", "Modal Logic", "The main modal concepts are necessity, possibility, impossibility, and contingency. All of these can be understood in terms of the concept of necessity."),
    ("Probability is a modal property.", "Modal Logic", "I believe that the property of being probably true is a modal property."),
    ("Necessity is analyticity.", "Analyticity", "Necessary truth is analytic truth; necessity is analyticity."),
    ("Analyticity is a property of propositions, not sentences.", "Analyticity", "We will use the word 'analytic' to denote a property of propositions, not sentences."),
    ("Sentence-analyticity diverges from proposition-analyticity.", "Analyticity", "Sentence-analyticity diverges from proposition-analyticity."),
    ("Analytic truths are non-empirical.", "Analyticity", "Analytic truths are true no matter what."),
    ("Analytic truth is high-resolution structural truth.", "Analyticity", "Analytic truth is truth in virtue of structure along with substructure."),
    ("Language mirrors propositional structure.", "Philosophy of Language", "Sentential structure mirrors propositional structure."),
    ("Analytic truths are true in virtue of micro-structure.", "Analyticity", "For a proposition to be analytically true is for it to be true in virtue of its structural and its substructural properties."),
    ("Quine denied informal analytic truth.", "Quine", "W.V.O. Quine says that, with a few trivial exceptions, there is no such thing as sentential analytic truth."),
    ("Quine argued analyticity is circularly defined.", "Quine", "Quine concludes, the concept of analyticity is viciously circular and therefore incoherent."),
    ("Quine was wrong about synonymy as the basis of analyticity.", "Quine", "Quine is wrong to hold that analyticity is to be understood in terms of synonymy."),
    ("Analytic truth is non-empirical truth.", "Analyticity", "Analytic truth is non-empirical truth."),
    ("Quine's position is self-defeating.", "Quine", "The view that there are no analytic statements is self-defeating."),
    ("Without analytic truth, nothing confirms anything.", "Analyticity", "If all truth were empirical, then nothing could confirm anything."),
    ("Some truths are contingent.", "Modal Logic", "It seems clear that some truths are contingent."),
    ("The denial of necessary truth is self-undermining.", "Modal Logic", "The assumption that no propositions are necessarily true is self-undermining."),
    ("Knowledge of necessary truth is needed for contingent knowledge.", "Epistemology", "Knowledge of necessary truths is a prerequisite for knowledge of contingent truth."),
    ("Quine's empiricism led him to reject analytic truth.", "Quine", "Quine's real reason for denying the existence of analytic truth lay in his staunch empiricism."),
    ("Empiricism collapses without non-observational knowledge.", "Epistemology", "There is necessarily a non-observational component to the acquisition of scientific knowledge."),
    ("Recognizing resemblances requires necessary truths.", "Epistemology", "Knowledge of necessary truths is a precondition for being able to recognize resemblances between things."),
    ("Proof requires necessity.", "Logic", "There are no proofs if all truth is contingent."),
    ("Analytic truth is not formal truth.", "Analyticity", "Formal truth isn't analytic truth."),
    ("Analytic statements have incoherent negations.", "Analyticity", "A statement is analytically true if its negation is incoherent."),
    ("Non-analytic truths are empirical.", "Analyticity", "Non-analytic truths are empirical truths."),
    ("Kant was wrong about synthetic a priori truths.", "Kant", "Kant infamously claimed that there are non-analytic truths that can be learned in a non-observational manner. He was wrong."),
    ("Sense-perception may trigger ratiocination without transmitting empirical content.", "Epistemology", "Sense-perception may trigger ratiocination without transmitting empirical content."),
    ("Analytic knowledge is justified by insight, not observation.", "Epistemology", "Your acceptance of DN can be justified only by insight into its meaning."),
    ("Sentence meaning is empirical; propositional content may be analytic.", "Philosophy of Language", "It's an empirical truth that the sentence 'squares have four sides' means what it does… but it's an analytic fact that squares have four sides."),
    ("There are non-trivial analytic truths.", "Analyticity", "There are non-trivial analytic truths."),
    ("No synthetic non-empirical truths exist.", "Analyticity", "Any non-analytic truth is empirical."),
    ("Formal truth is syntactic truth.", "Logic", "Formal truth is syntactic truth. A sentence is 'syntactically true' if, given only its syntactic structure, it cannot fail to be true."),
    ("Quine defined formal truth via logical constants.", "Quine", "A sentence S is formally true if, given any expression in S that isn't a logical constant, it isn't possible to produce a false sentence by replacing that expression."),
    ("Quine's list of logical constants is arbitrary.", "Quine", "Quine's analysis is vitiated by his failing to say what conditions an expression must satisfy to be a 'logical constant.'"),
    ("Formal truth is not topic-neutral truth.", "Logic", "Formal truth ≠ topic-neutral truth."),
    ("Formal truth is instance of universally true open-sentence.", "Logic", "A sentence is formally true if it's an instance of a universally true open-sentence."),
    ("Logical constants are expressions in pure universally true open-sentences.", "Logic", "A 'logical constant' is any expression other than a variable that occurs in a pure, universally true open-sentence."),
    ("Not all analytic truth is formal truth.", "Analyticity", "Not all analytic truth is formal truth."),
    ("Wittgenstein was wrong: analytic truth ≠ formal truth.", "Wittgenstein", "Wittgenstein's thesis that all analytic truth is formal truth is not only wrong but incoherent."),
    ("No conceptual analysis is formally true.", "Analyticity", "No conceptual analysis is formally true."),
    ("Analytic statements are universal generalizations or instances.", "Analyticity", "Conceptual analyses are expressed by analytic statements, and analytic statements either coincide with informal analytic universal generalizations or are instances of such generalizations."),
    ("Pre-semantic information affects conveyed meaning.", "Philosophy of Language", "Pre-semantic information can have an incalculably profound effect on what is conveyed by utterances."),
    ("Kripke's examples confuse semantic and pre-semantic content.", "Modal Logic", "Kripke and, after him, many others have professed to find many examples of non-analytic necessary truths; but in each case… semantics is being confused with pre-semantics."),
    ("Necessity is the central modal concept.", "Modal Logic", "Necessity is the most important modal concept."),
    ("Quine's empiricism is self-refuting.", "Quine", "The view that there is no analytic truth entails that there is analytic truth, and is therefore self-refuting."),
    ("The supposition that all truth is empirical is viciously regressive.", "Epistemology", "The supposition that all truth is empirical is viciously regressive."),
    ("Behaviorism is false.", "Philosophy of Mind", "Behaviorism is false."),
    ("Chomsky's innatism opposes Quine's behaviorism.", "Linguistics", "Chomsky proposed an alternative theory, according to which inborn cognitive structures are largely determinative of how we learn and use language."),
    ("Empiricism is inconsistent with empirical evidence.", "Epistemology", "Empiricism is therefore inconsistent with empirical evidence of the most blatant and widespread kind."),
    ("All denial of analytic truth stems from empiricism.", "Epistemology", "All philosophers, and indeed non-philosophers, who deny the existence of analytic truth do so because they are staunch empiricists."),
    ("Observation alone cannot yield interpretation.", "Epistemology", "It is totally incoherent to suppose that one could know on the basis of observation alone how to interpret the data of observation."),
    ("Abstract resemblance requires necessary knowledge.", "Epistemology", "One cannot discern any abstract similarities between any two concrete situations unless one knows… what conditions must be fulfilled."),
    ("To prove something is to show it must be the case.", "Logic", "To prove conclusion C on the basis of premises P is to show it to be necessarily true that if P, then C."),
    ("Empirical truths require observational justification.", "Epistemology", "If, in order to justify acceptance of S, you must cite empirical data, it's empirical."),
    ("Sense-perception can trigger non-empirical knowledge.", "Epistemology", "Sense-perception may well have been needed to initiate or trigger the reflections on the basis of which you learned DN."),
    ("Sentence meaning is contingent; propositional content may be necessary.", "Philosophy of Language", "It's an empirical fact that the sentence 'squares have four sides' means what it does… but it's an analytic fact that squares have four sides."),
    ("Quine's synonymy account of analyticity fails.", "Quine", "Quine is wrong to hold that analyticity is to be understood in terms of synonymy."),
    ("Kripke's argument is a massive non-sequitur.", "Modal Logic", "Kripke's argument involves a massive non-sequitur."),
    ("Rigid designators refer to the same object in all possible worlds.", "Modal Logic", "Rigid designators refer to the same object in all possible worlds."),
    ("Negative existentials are metalinguistic.", "Logic", "Statements of non-existence attribute falsity to propositions."),
    ("Quine's linguistic behaviorism is incoherent.", "Quine", "Quine's linguistic behaviorism is incoherent and inconsistent with evidence."),
    ("Innate structures explain language acquisition.", "Linguistics", "Chomsky's innatism is supported by empirical evidence."),
    ("Proof establishes necessary consequence.", "Logic", "Proof shows that a conclusion necessarily follows from premises."),
    ("Proper names refer directly without descriptive content.", "Philosophy of Language", "Proper names refer directly without descriptive content."),
    ("Modal operators apply to propositions.", "Modal Logic", "Necessity and possibility are operators on propositions."),
    ("Existence statements assess whether any object satisfies a description.", "Logic", "Existence statements assess whether any object satisfies a description."),
    ("Kripke mistakes epistemology for modal status.", "Modal Logic", "Kripke mistakes how we come to know an identity for its modal status."),
    ("Human cognition requires innate conceptual structures.", "Philosophy of Mind", "Human cognition requires innate conceptual structures."),
    ("Scientific reasoning depends on necessary truths not derived from observation.", "Epistemology", "Scientific reasoning depends on necessary truths not derived from observation."),
    ("Identifying properties requires knowledge of necessary conditions.", "Epistemology", "Identifying properties requires knowledge of necessary conditions."),
    ("Proof shows a conclusion is necessarily true given premises.", "Logic", "Proof shows that a conclusion is necessarily true given the premises."),
    ("Analytic truths are known independently of experience.", "Epistemology", "Analytic truths are known independently of experience."),
    ("Formal truths are substitution instances of logical laws.", "Logic", "Formal truths are substitution instances of logical laws."),
    ("Quine's list of logical constants lacks a theoretical basis.", "Quine", "Quine's list of logical constants lacks a theoretical basis."),
    ("Conceptual analyses are expressed by analytic sentences that are not formal truths.", "Analyticity", "Conceptual analyses are expressed by analytic sentences that are not formal truths."),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_ap_num = 0
    for pid in existing_ids:
        if pid.startswith('AP-'):
            try:
                num = int(pid.split('-')[1])
                max_ap_num = max(max_ap_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_ap_num + 1
    
    for pos_text, topic, quote in ch18_positions:
        pos_id = f"AP-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"AP-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Analytic Philosophy Ch18 - J.-M. Kuczynski",
            "work_id": "WORK-ANALYTIC-CH18",
            "domain": "analytic_philosophy"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Analytic Philosophy Ch18: +{len(new_positions)} positions"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 24,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Analytic Philosophy Ch18",
            "positions": len(new_positions),
            "topics": ["Modal Logic", "Analyticity", "Kripke", "Quine", "Wittgenstein", "Epistemology"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Analytic Philosophy Ch18 positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: AP-{max_ap_num+1:03d} to AP-{counter-1:03d}")

if __name__ == "__main__":
    main()
