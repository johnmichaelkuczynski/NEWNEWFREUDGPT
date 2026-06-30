#!/usr/bin/env python3
"""
Add Determinism batch 2 positions to the Kuczynski database.
"""

import json
from datetime import datetime

determinism_batch2 = [
    ("The view that the future is 'fixed' by the present is a defining claim of determinism.", "Determinism"),
    ("Indeterminism is a minimal negation of determinism, requiring only one instance of non-determination.", "Indeterminism"),
    ("Most of the observable, macro-scale world operates as if it were deterministic.", "Determinism"),
    ("Apparent randomness in everyday life usually results from complexity and ignorance, not fundamental indeterminacy.", "Randomness"),
    ("The principle of 'same cause, same effect' is central to the deterministic worldview.", "Determinism"),
    ("Even if micro-level events are indeterministic, their effects often cancel out or are irrelevant at macro scales.", "Determinism"),
    ("Predictability is a practical, epistemic concept, while determinism is a metaphysical one.", "Determinism vs Predictability"),
    ("The limits of predictability are logical, not merely technological.", "Unpredictability"),
    ("Sense-perception is an invasive, information-gathering process.", "Perception and Reality"),
    ("The chain of perception—from object to light to eye to brain—involves multiple transformative stages.", "Perception and Reality"),
    ("Information carried by light is a snapshot of the past state of an object.", "Perception and Reality"),
    ("Any interaction between a probe (like light) and an object alters the object, however slightly.", "Perception and Reality"),
    ("For very small objects, the act of observation can dramatically change their state.", "Perception and Reality"),
    ("The observer cannot precisely know the perturbation caused by the observation itself.", "Perception and Reality"),
    ("Therefore, there is an inescapable 'margin of error' between reality and perception.", "Perception and Reality"),
    ("Attempting to correct this error through further interaction only introduces more perturbation.", "Perception and Reality"),
    ("This perceptual dilemma applies to any entity that gains knowledge through causal interaction.", "Epistemology"),
    ("The author explicitly rejects the notion of non-causal, direct knowledge (even for a deity).", "Epistemology"),
    ("Knowledge requires justification, which requires evidence, which requires a causal link.", "Epistemology"),
    ("A 'correct hallucination' or lucky guess does not constitute knowledge.", "Epistemology"),
    ("Logical truths (like the laws of logic) are not limitations on power but define what is coherent.", "Logic"),
    ("God's inability to have non-causal knowledge is akin to an athlete's inability to score a football touchdown in a soccer game—it's a category error.", "Epistemology"),
    ("Prediction is an application of causal laws to known initial conditions.", "Prediction"),
    ("Inaccurate knowledge of initial conditions guarantees inaccurate predictions.", "Prediction"),
    ("Our own mental states and knowledge are part of the causal fabric of the world.", "Knowledge and Action"),
    ("The content of our future knowledge is a future fact that can affect present actions.", "Knowledge Growth"),
    ("Knowing your future knowledge now would change that future knowledge, creating a paradox.", "Knowledge Growth"),
    ("Therefore, the growth of personal knowledge is an inherently unpredictable process.", "Knowledge Growth"),
    ("The 'infallible self-predictor' is a logically incoherent concept.", "Self-Prediction"),
    ("Psychological attitudes like confidence can be causal factors in bringing about outcomes.", "Self-Prediction"),
    ("Self-fulfilling prophecies demonstrate that predictions can be part of the causal chain leading to the predicted event.", "Self-Prediction"),
    ("This complicates prediction because the prediction itself becomes a new initial condition.", "Self-Prediction"),
    ("'Random' in common parlance means 'unforeseen' or 'unexpected given my knowledge,' not 'acausal.'", "Randomness"),
    ("An event can be fully determined yet perfectly random from a limited epistemic perspective.", "Randomness"),
    ("Randomness is not in the event but in the relationship between the event and an information set.", "Randomness"),
    ("Two observers with different knowledge can disagree on whether an event is random.", "Randomness"),
    ("In an indeterministic scenario with two equally likely outcomes, the actual outcome is not random relative to the knowledge that one of them would occur.", "Randomness"),
    ("Indeterminism can exist without events seeming 'random' to a knowledgeable observer.", "Indeterminism"),
    ("The verification of universal claims like 'all metals expand' requires inductive inference.", "Induction"),
    ("Hume's problem of induction questions the rational justification for such inferences.", "Induction"),
    ("In practice, everyone accepts inductive reasoning as justified.", "Induction"),
    ("The difference between a justified belief (I won't sprout wings) and an unjustified one (it will rain gumdrops) is clear in practice.", "Induction"),
    ("Arguments against determinism based on the behavior of 'identical' clones fail because perfect microphysical identity is virtually impossible.", "Determinism"),
    ("Any two physical systems, no matter how similar, will have some differing initial conditions.", "Determinism"),
    ("Determinism only requires that *identical* initial conditions yield identical outcomes; it doesn't claim we can ever create them.", "Determinism"),
    ("Causal discovery in science works by observing correlations while striving to control other variables.", "Causation"),
    ("A perfect correlation (100%) in practice is not necessary to infer a deterministic underlying law.", "Causation"),
    ("Evidence for a deterministic law is found if the correlation can be made arbitrarily strong by controlling more factors.", "Causation"),
    ("Our evidence for deterministic laws is 'imperfect' but of the same type as our evidence for any empirical fact.", "Epistemology"),
    ("Nothing known through sense-perception can be 'definitively established' with absolute certainty.", "Epistemology"),
    ("The existence of your hands is no more certain, in a strict philosophical sense, than the existence of deterministic laws.", "Epistemology"),
    ("The shortcomings of induction are a general problem for empirical knowledge, not a specific problem for determinism.", "Induction"),
    ("We can have strong, reasonable certainty about deterministic laws.", "Determinism"),
    ("The text presents a sustained defense of 'compatibilism' between determinism and unpredictability.", "Determinism vs Predictability"),
    ("It argues against the intuitive link between determinism and complete predictability.", "Determinism vs Predictability"),
    ("It also argues against the intuitive link between indeterminism and randomness.", "Indeterminism"),
    ("The author positions their view as a 'close approximation' to the truth of determinism for the macro-world.", "Determinism"),
    ("The narrative example of Smith's death illustrates the core distinctions between determined, random, and foreseeable.", "Randomness"),
    ("The concept of 'independent causal sequences' is key to understanding common-sense randomness.", "Randomness"),
    ("The burden of proof is higher for the determinist than for the indeterminist.", "Determinism"),
    ("Modern physics has made determinism a 'live' philosophical question, not a settled one.", "Determinism"),
    ("Self-knowledge, specifically knowledge of one's own future states, is presented as particularly problematic for prediction.", "Self-Prediction"),
    ("The chapter implies that free will debates must account for these predictability limits.", "Free Will"),
    ("The 'perfect predictor' is often used in thought experiments about free will; this chapter undermines the coherence of that concept.", "Self-Prediction"),
    ("Information is physically embodied (in light waves, neural impulses).", "Information Theory"),
    ("Transmission of information takes time, creating a necessary lag.", "Information Theory"),
    ("Decoding information is a physical process in the perceiver.", "Information Theory"),
    ("The 'veil of perception' is a real, physical barrier created by the causal process of perception itself.", "Perception and Reality"),
    ("The term 'transperceptual' refers to the world as it exists outside of this perceptual process.", "Perception and Reality"),
    ("Scientific laws are about transperceptual correlations.", "Philosophy of Science"),
    ("Our evidence for these correlations is always 'imperfect' because it's filtered through perception.", "Epistemology"),
    ("The possibility of an 'accidentally correct' representation of the world is acknowledged but deemed irrelevant to knowledge.", "Epistemology"),
    ("Justification requires a reliable link between belief and truth, which causality provides.", "Epistemology"),
    ("The argument against divine foreknowledge is based on epistemic principles, not theological ones.", "Epistemology"),
    ("Much debate about determinism is muddled by conflating the metaphysical (what *is*) with the epistemic (what we can *know*).", "Determinism vs Predictability"),
    ("The author is a realist about the external world and causal laws.", "Metaphysics"),
    ("They are also a fallibilist about our knowledge of that world.", "Epistemology"),
    ("The view presented is naturalistic, explaining knowledge and perception within a physical, causal framework.", "Naturalism"),
    ("It rejects Cartesian-style dualism or direct mental access to the world.", "Philosophy of Mind"),
    ("The 'gulf' between perception and reality is not an argument for skepticism but a logical constraint on prediction.", "Perception and Reality"),
    ("The focus is on the *conditions for the possibility* of prediction, which are found to be logically limited.", "Prediction"),
    ("The chapter can be seen as an application of broader insights about information theory and observer effects to classic philosophical problems.", "Information Theory"),
    ("Laplace's demon—an infinitely intelligent predictor knowing all initial conditions and laws—is logically impossible, not just physically impossible.", "Determinism"),
    ("A deterministic universe is not a 'clockwork' universe knowable in its entirety by any internal observer.", "Determinism"),
    ("This is due to the very nature of what it means to be an observing part of that causal system.", "Epistemology"),
    ("The author uses analogies from sports (football/soccer) to illustrate logical incoherence.", "Methodology"),
    ("The text is pedagogical, addressing common student arguments directly.", "Methodology"),
    ("One exercise question references the Heisenberg Uncertainty Principle, suggesting it is often mistakenly invoked in these debates.", "Unpredictability"),
    ("The author claims their personal experience validates the power of self-fulfilling prophecy (self-confidence).", "Self-Prediction"),
    ("They also speculate that apparent self-doubt might sometimes be a strategic form of self-protection.", "Self-Prediction"),
    ("Examples are used extensively to ground abstract philosophical points (Smith, the elevator, the metal bar, the cloned cells).", "Methodology"),
    ("The chapter aims to clarify common misconceptions in philosophy of science and epistemology.", "Philosophy of Science"),
    ("The ultimate conclusion is that a deterministic universe is not knowable in its entirety by any internal observer, due to the nature of observation itself.", "Determinism vs Predictability"),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_det_num = 0
    for pid in existing_ids:
        if pid.startswith('DET-'):
            try:
                num = int(pid.split('-')[1])
                max_det_num = max(max_det_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_det_num + 1
    
    for pos_text, topic in determinism_batch2:
        pos_id = f"DET-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"DET-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "source": "Determinism, Randomness, and Unpredictability - J.-M. Kuczynski",
            "work_id": "WORK-DET-RAND",
            "domain": "metaphysics"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Determinism Batch 2: +{len(new_positions)} positions"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 18,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Determinism, Randomness, and Unpredictability (Ch. 14) - Batch 2",
            "positions": len(new_positions),
            "topics": ["Determinism", "Randomness", "Epistemology", "Information Theory", "Free Will"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Determinism (batch 2) positions.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: DET-{max_det_num+1:03d} to DET-{counter-1:03d}")

if __name__ == "__main__":
    main()
