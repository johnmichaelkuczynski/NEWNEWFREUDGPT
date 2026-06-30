#!/usr/bin/env python3
"""
Add Determinism, Randomness, and Unpredictability positions to the Kuczynski database.
Source: Chapter 14 of Kuczynski's work
"""

import json
from datetime import datetime

determinism_positions = [
    ("Determinism is the view that how the world is at any given point in time fixes how it will be in every respect at all later times.", "Determinism"),
    ("Given how the world is now, there is only one way it could possibly be in the future.", "Determinism"),
    ("Indeterminism is the doctrine that determinism is false.", "Indeterminism"),
    ("Indeterminism is not the view that the world is chaotic or lawless.", "Indeterminism"),
    ("For indeterminism to be true, there needs to be only one 'renegade' event.", "Indeterminism"),
    ("Determinism is a much stronger and harder claim to establish than indeterminism.", "Determinism"),
    ("It is an open question whether the world is strictly deterministic at the sub-atomic level.", "Determinism"),
    ("For most intents and purposes, the world of 'medium-sized' objects is deterministic.", "Determinism"),
    ("Determinism and predictability are not the same thing.", "Determinism vs Predictability"),
    ("A completely indeterministic system is unpredictable.", "Unpredictability"),
    ("A deterministic system may also be unpredictable.", "Unpredictability"),
    ("Perceiving the world necessarily involves changing it, creating a gulf between perception and reality.", "Perception and Reality"),
    ("Information gained through sense-perception is always dated.", "Perception and Reality"),
    ("The object of perception is altered by the act of perceiving it.", "Perception and Reality"),
    ("Attempting to narrow the perceptual gulf by gathering more information only widens it.", "Perception and Reality"),
    ("The logical conditions for sense-perception apply to any percipient being, including God.", "Perception and Reality"),
    ("Knowledge requires causal connections to serve as evidence.", "Epistemology"),
    ("God could not have knowledge of a spatiotemporal entity without being causally connected to it.", "Epistemology"),
    ("The laws of logic apply to God.", "Logic and Theology"),
    ("Prediction requires knowledge of initial conditions and causal laws.", "Prediction"),
    ("One's knowledge of initial conditions is necessarily inaccurate, so predictions will be off.", "Prediction"),
    ("What we know affects what we do, and what we do affects how the world is.", "Knowledge and Action"),
    ("One cannot know now what one will know in the future.", "Knowledge Growth"),
    ("The growth of one's knowledge affects the world, making complete prediction impossible even under determinism.", "Knowledge Growth"),
    ("The concept of an infallible self-predictor is incoherent.", "Self-Prediction"),
    ("Self-fulfilling prophecies and self-defeating viewpoints exist.", "Self-Prediction"),
    ("Self-predictions affect the future, thus undermining their own predictive accuracy.", "Self-Prediction"),
    ("'Random' does not mean 'uncaused.'", "Randomness"),
    ("Random events are caused, but their causes are unforeseeable.", "Randomness"),
    ("Randomness is a relation an event has to a given body of knowledge, not an intrinsic property of the event.", "Randomness"),
    ("There can be random events in a deterministic world.", "Randomness"),
    ("In an indeterministic world, events are not necessarily random.", "Randomness"),
    ("Randomness is a property of statements (or relations between statements), not of events.", "Randomness"),
    ("Many universal statements (e.g., 'all metal expands when heated') cannot be definitively verified by observation alone.", "Verification"),
    ("Determinism ('all events have complete causes') is similarly unverifiable in a strict observational sense.", "Verification"),
    ("The unverifiability of determinism, in this sense, is a trivial point shared with all empirical generalizations.", "Verification"),
    ("If inference rules are allowed, universal generalizations like determinism can be verified.", "Verification"),
    ("Saying something 'could' happen contrary to a law often only means it isn't logically ruled out by current knowledge, not that it is physically possible.", "Possibility"),
    ("Hume's argument against the rationality of induction is difficult to refute but is not accepted in practice.", "Induction"),
    ("The belief that one will not sprout wings is justified, unlike a belief that it will rain gumdrops tomorrow.", "Induction"),
    ("An argument against determinism based on cloned cells behaving differently fails because cells are never microphysically identical.", "Determinism"),
    ("Different initial conditions lead to different outcomes, which is consistent with determinism, not a refutation of it.", "Determinism"),
    ("Causal connections are discovered by observing correlations between changes in initial conditions and changes in outcomes.", "Causation"),
    ("One cannot replicate initial conditions perfectly, but one can hold other factors constant to observe causal links.", "Causation"),
    ("A deterministic connection means the likelihood of an outcome approaches 100% as other factors are controlled.", "Determinism"),
    ("Experience can provide good evidence for strictly deterministic connections.", "Determinism"),
    ("We can have imperfect evidence for perfect (deterministic) correlations.", "Epistemology"),
    ("Deterministic laws are no less capable of being established with reasonable certainty than any other fact about the external world.", "Determinism"),
    ("The limitations of induction are not a special problem for establishing causality.", "Induction"),
    ("'Verification' defined as purely observational renders most knowledge of the external world unverifiable.", "Verification"),
    ("The gulf between perception and reality is a necessary consequence of how perception works.", "Perception and Reality"),
    ("Any attempt to correct perceptual distortion introduces further distortion.", "Perception and Reality"),
    ("The information-carrier (e.g., light) alters the object it interacts with.", "Perception and Reality"),
    ("The perceiver cannot know the exact nature of the changes inflicted on the object by the information-gathering process.", "Perception and Reality"),
    ("Therefore, what is perceived is always different from what exists at the moment of perception.", "Perception and Reality"),
    ("The argument applies to any sensory modality, not just vision.", "Perception and Reality"),
    ("The claim that God could have non-causal knowledge is incoherent, akin to scoring a touchdown in soccer.", "Epistemology"),
    ("For a mental state to be evidence of an external thing, it must be an effect of that thing.", "Epistemology"),
    ("Justification for belief requires evidence, which requires a causal connection.", "Epistemology"),
    ("A belief based on a lucky guess, even if true, is not knowledge.", "Epistemology"),
    ("Causal connections are inherently disruptive.", "Causation"),
    ("Therefore, God's mental representations of the world must, in some cases, be discrepant with reality.", "Epistemology"),
    ("Learning about the world changes it.", "Knowledge and Action"),
    ("Predictions are based on outdated information about initial conditions.", "Prediction"),
    ("The second reason for the predictability/determinism gap is that knowledge states affect the world.", "Knowledge and Action"),
    ("If you knew now what you would know in 10 years, that knowledge would already be part of your present state, changing the future.", "Knowledge Growth"),
    ("One's future knowledge cannot be incorporated into present knowledge without altering what that future knowledge would be.", "Knowledge Growth"),
    ("Therefore, the growth of knowledge is inherently unpredictable.", "Knowledge Growth"),
    ("Self-confidence can breed success, acting as a self-fulfilling prophecy.", "Self-Prediction"),
    ("Unwarranted pessimism can breed failure.", "Self-Prediction"),
    ("The self-fulfilling nature of predictions opens a gap between how things will be and how we can know them to be.", "Self-Prediction"),
    ("Predictions about one's own predictions further complicate prediction.", "Self-Prediction"),
    ("An event is 'random' relative to a body of knowledge if its occurrence could not reasonably be predicted from that knowledge.", "Randomness"),
    ("Randomness is epistemic, not ontological.", "Randomness"),
    ("Smith's death by ceiling lamp was determined but random relative to the narrator's knowledge.", "Randomness"),
    ("To a building inspector with different knowledge, the same event was not random.", "Randomness"),
    ("In an indeterministic scenario with equiprobable outcomes, the actual outcome is not 'random' relative to the knowledge of the possible outcomes.", "Randomness"),
    ("An event can be both random (relative to one knowledge set) and non-random (relative to another).", "Randomness"),
    ("Indeterminism does not entail widespread randomness.", "Indeterminism"),
    ("The amount of randomness in an indeterministic world is not necessarily great.", "Indeterminism"),
    ("Universal generalizations are not falsified by the practical impossibility of perfect verification.", "Verification"),
    ("The charge that determinism is unverifiable often rests on an overly strict definition of 'verification.'", "Verification"),
    ("Common sense and scientific practice accept inference-based verification.", "Verification"),
    ("The possibility of the next metal sample not expanding is a logical, not a physical, possibility.", "Possibility"),
    ("We know, inductively, that metal expands when heated, and this knowledge is justified.", "Induction"),
    ("The cloned-cell argument mistakenly assumes biological identity implies microphysical identity.", "Determinism"),
    ("Microphysical differences guarantee different outcomes, which is consistent with determinism.", "Determinism"),
    ("The argument that initial conditions are never identical is true but irrelevant to establishing causal laws.", "Causation"),
    ("Causal laws are established by observing correlations under controlled conditions.", "Causation"),
    ("The correlation between cause and effect can approach perfection as confounding factors are eliminated.", "Causation"),
    ("Technological limitations do not preclude evidence for deterministic laws.", "Determinism"),
    ("Evidence for deterministic laws is of the same kind and quality as evidence for other empirical regularities.", "Determinism"),
    ("The Heisenberg Uncertainty Principle is not directly relevant to the logical arguments about auto-prediction.", "Unpredictability"),
    ("The unpredictability of our own future knowledge is a logical, not a quantum-mechanical, limitation.", "Self-Prediction"),
    ("Even a maximally intelligent being with perfect senses could not predict everything in a deterministic world.", "Unpredictability"),
    ("Reason #1 (perception alters the world) and Reason #2 (knowledge growth affects the world) establish this.", "Unpredictability"),
    ("The very act of gathering information for a prediction changes the system being predicted.", "Prediction"),
    ("Therefore, complete self-prediction or world-prediction is logically impossible.", "Self-Prediction"),
    ("Determinism is a metaphysical claim about causality; unpredictability is an epistemological claim about knowledge.", "Determinism vs Predictability"),
    ("The world can be both deterministic and fundamentally unpredictable to any knowing agent within it.", "Determinism vs Predictability"),
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
    
    for pos_text, topic in determinism_positions:
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
    data['database_metadata']['latest_addition'] = f"Determinism, Randomness, and Unpredictability: +{len(new_positions)} positions"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 17,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Determinism, Randomness, and Unpredictability (Ch. 14)",
            "positions": len(new_positions),
            "topics": ["Determinism", "Indeterminism", "Randomness", "Unpredictability", "Causation", "Perception"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Determinism/Randomness positions.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: DET-{max_det_num+1:03d} to DET-{counter-1:03d}")

if __name__ == "__main__":
    main()
