#!/usr/bin/env python3
"""
Add Chapter 17 Analytic Philosophy positions with quotes to the Kuczynski database.
"""

import json
from datetime import datetime

analytic_positions = [
    ("Events cause other events to occur.", "Causation", "Events cause other events to occur."),
    ("Some philosophers have denied the existence of causation.", "Causation", "Astonishingly, some philosophers have denied the existence of causation."),
    ("Empiricism holds that all knowledge is strictly observation based.", "Empiricism", "According to empiricism, all knowledge is strictly observation based."),
    ("Empiricists believe we cannot see or otherwise observe causal ties.", "Empiricism", "According to many empiricists, we cannot see or otherwise observe causal ties."),
    ("The argument against causal ties involves a major non-sequitur.", "Causation", "But this argument involves a major non-sequitur."),
    ("We don't observe electrons or quarks, but we have good reason to believe them to exist.", "Epistemology", "We don't observe electrons or quarks, but we have good reason to believe them to exist."),
    ("Causal ties, if they exist, are occupants of space-time.", "Causation", "Causal ties, if they exist, are occupants of space-time, like rocks and vases and chairs"),
    ("The concept of persistence is itself a causal notion.", "Causation", "The concept of persistence is itself a causal notion"),
    ("We observe causal sequences whenever we observe anything.", "Causation", "Thus, we observe causal sequences whenever we observe anything."),
    ("The contention that we don't observe causal ties is of doubtful accuracy and questionable coherence.", "Causation", "Although it has been enormously influential, it's of doubtful accuracy, it's of questionable coherence."),
    ("The very notion of spatial occupancy is a causal notion.", "Causation", "For example, the very notion of spatial occupancy is a causal notion"),
    ("Malleability and conductivity are causal properties.", "Causation", "Malleability and conductivity are causal properties."),
    ("To describe an object as made of steel is to say it will react to situations in certain ways.", "Causation", "Thus, to describe a given object as being of made of steel is to say that, other things being equal, it will react to situations in ways in which it wouldn't otherwise react."),
    ("Anything that says anything about the spatiotemporal world has causal content.", "Causation", "For that reason, anything that says anything about anything in the spatiotemporal world has causal content."),
    ("Only events can be causes, not objects.", "Causation", "First of all, it is only events that can be causes. Objects are not causes."),
    ("The rock did not cause the window to break, but an event involving the rock did.", "Causation", "The rock didn't cause the window to break. What did so was some event involving the rock"),
    ("Non-causes may have causal properties.", "Causation", "Non-causes may have causal properties."),
    ("Not every property of a rock is a cause.", "Causation", "Not every property of the rock is a cause."),
    ("A condition is a relatively persistent state.", "Causation", "A condition is a relatively persistent state (e.g., the room's having a certain temperature)."),
    ("An event is a change in conditions.", "Causation", "An event is a change in conditions."),
    ("Conditions can be causes.", "Causation", "But conditions themselves seem to be causes."),
    ("An event is a change, whereas a condition is the absence of change.", "Causation", "An event is, by definition, a change, whereas a condition is, it would seem, the absence of change."),
    ("Conditions consist of events.", "Causation", "This argument overlooks the fact that conditions consist of events."),
    ("The water's having a given temperature consists in its particles having certain kinetic properties.", "Causation", "The water's having a given temperature consists in its containing particles that have certain kinetic properties."),
    ("There is no heat where there are no events.", "Causation", "There is no heat where there are no events."),
    ("A person's being healthy consists of metabolic events.", "Causation", "A person's being healthy consists in that person's body doing what it should."),
    ("There is no life and no health where there are no metabolic events.", "Causation", "There is no life, and therefore no health, where there are no metabolic events."),
    ("Changes may be internal to conditions of changelessness.", "Causation", "And although events do necessarily constitute changes, those changes may be, and often are, internal to conditions of changelessness."),
    ("Nothing non-spatiotemporal can be a cause.", "Causation", "Nothing non-spatiotemporal can be a cause."),
    ("There are causes only where there are changes, and changes happen in time.", "Causation", "There are causes only where there are changes, and changes happen in time."),
    ("Universals, if they exist, are causally impotent.", "Universals", "So universals, if they exist, are causally impotent."),
    ("There must be some kind of causal connection between two things if one is to know of the other.", "Epistemology", "The idea is that there must be some kind of a causal connection between two things if one of them is to know of the other."),
    ("There is never awareness where there isn't a causal nexus.", "Epistemology", "One obvious way to generalize this line of reasoning is to say that there is never awareness where there isn't a causal nexus."),
    ("A causal connection between two things by itself does not mediate awareness of the other.", "Epistemology", "under no circumstances does a causal connection between two things by itself mediate the one's having an awareness of the other."),
    ("There is always a non-causal component to awareness, even to sense-perception.", "Epistemology", "There is always a non-causal component to awareness, even to sense-perception."),
    ("We do have good reasons to countenance the existence of universals.", "Universals", "we do have good reasons to countenance the existence of universals, and no good reasons not to."),
    ("The complete cause of anything is very hard to identify.", "Causation", "The complete cause of anything is very hard to identify."),
    ("Whether anything other than the entire state of the universe can be the complete cause is debatable.", "Causation", "It is a matter of philosophical and scientific debate whether, given an event E happening at t, anything other than the entire state of the universe just prior to t can be the complete cause of E."),
    ("Aristotle distinguished between four kinds of causality: efficient, final, material, and formal.", "Causation", "Aristotle distinguished between four different kinds of causality: efficient, final, material, and formal."),
    ("x is the efficient cause of y if x makes y happen.", "Causation", "x is the efficient cause of y if x makes y happen."),
    ("x is the final cause of y if y is an action and x is the creature's objective in performing y.", "Causation", "x is the final cause of y if y is an action on the part of some creature and x is that creature's objective in performing y."),
    ("x is the material cause of y if x is the material that y is made of.", "Causation", "x is the material cause of y if x is the material that y is made of."),
    ("x is the formal cause of y if x is y's form.", "Causation", "x is the formal cause of y if x is y's form."),
    ("A property is essential to a thing if it cannot lose that property without ceasing to exist.", "Essentialism", "a property is essential to a given thing if that thing could not lose that property without for that very reason ceasing to exist."),
    ("The dependence-relation between essences and things is logical or constitutive, not causal.", "Essentialism", "The dependence-relation in question is not of a causal nature, and is instead of a logical or constitutive nature."),
    ("Aristotle's belief in essences is incoherent.", "Essentialism", "Aristotle's belief that things have essences is an incoherent one,"),
    ("Dependence-relations hold between events or statements, not objects.", "Causation", "Contrary to what Aristotle thought, dependence-relations don't hold between objects. They hold between events or between statements."),
    ("The concept of formal causes is incoherent.", "Causation", "Thus, the concept of a formal cause is an incoherent one."),
    ("The concept of material causes is incoherent.", "Causation", "So, for the same reason, is the concept of a material cause."),
    ("The concept of efficient causality is coherent.", "Causation", "The concept of efficient causality clearly is a coherent one."),
    ("Efficient causality is the most fundamental form of causality.", "Causation", "But it's the most fundamental one."),
    ("Goals per se are abstract objects and do no causal work.", "Causation", "Goals are abstract objects and therefore do no causal work."),
    ("A person's having a goal does causal work.", "Causation", "What does do causal work is a given person's having a given goal."),
    ("Goals per se are propositions and not causes.", "Causation", "In general, goals per se, being propositions, aren't causes at all."),
    ("A person's having a goal is an efficient cause.", "Causation", "But my having a goal is a garden-variety efficient cause."),
    ("States of affairs, not objects, have effects.", "Causation", "it is states of affairs (or events), not objects, that have effects;"),
    ("Propositions, not objects, stand in dependence-relations.", "Causation", "it is propositions, not objects, that stand in dependence-relations."),
    ("Functionalism has no plausibility for sensations or anything with phenomenal content.", "Functionalism", "Functionalism has no plausibility when it comes to sensations or, more generally, anything that has phenomenal content."),
    ("Functionalism cannot accommodate the fact that mental states cause behavior.", "Functionalism", "But functionalism cannot accommodate this obvious fact"),
    ("According to functionalism, causal relations fix the content of mental states.", "Functionalism", "According to functionalism, it is in virtue of what x causes and what causes it that x is a belief"),
    ("Functionalism implies that mental states have no causal powers.", "Functionalism", "if functionalism is correct, then the mental does nothing; it has no causal powers at all"),
    ("Functionalism denies the very existence of minds.", "Functionalism", "functionalism denies the very existence of minds"),
    ("Content-externalism posits that two identical people can have thoughts with different contents due to different causal histories.", "Content-Externalism", "two people, Smith and Twin-Smith, who are exactly the same, can have thoughts with different contents"),
    ("Content-externalism is incoherent.", "Content-Externalism", "This view is incoherent"),
    ("If Smith and Twin-Smith switched places, they would not behave or think differently.", "Content-Externalism", "If Smith and Twin-Smith were to switch places, neither would behave or think differently from how he would otherwise do so"),
    ("Content-externalism embodies a failure to appreciate the concept 'in virtue of'.", "Content-Externalism", "Content-externalism embodies a failure to appreciate the concept meant by the phrase 'in virtue of'"),
    ("Tyler Burge's revision of causality to accommodate content-externalism is ad hoc and unnecessary.", "Content-Externalism", "This position borders on incoherence. It's brazenly ad hoc. And it's unnecessary, since the data is easily modeled without it"),
    ("Two worlds cannot differ with respect to a single event without differing in all causal antecedents.", "Counterfactuals", "Two worlds cannot differ with respect to a single event unless they differ with respect to all of the causal antecedents of those events."),
    ("Counterfactuals are identical with causal statements.", "Counterfactuals", "If we're right, counterfactuals are identical with causal statements."),
    ("According to Hume, nothing makes anything happen.", "Hume", "According to David Hume, nothing makes anything happen."),
    ("If Hume is right, it's hard to see how anything could cause anything to happen.", "Hume", "If Hume is right, it's hard to see how anything could, in any real sense, cause anything to happen."),
    ("Lewis accepts Hume's analysis.", "Lewis", "David Lewis accepts Hume's analysis."),
    ("Lewis and Hume are hardcore empiricists and reject the idea of forces.", "Lewis", "like Hume, Lewis is a hardcore empiricist and rejects the idea that there are forces."),
    ("Lewis thinks denying causality goes too far.", "Lewis", "But Lewis rightly thinks that denying the existence of causality is going too far."),
    ("We can't sense-perceive what is going on in other possible worlds.", "Lewis", "We obviously can't see or otherwise sense-perceive what is going on in other worlds."),
    ("Our knowledge of counterfactual truths is not based on other worlds.", "Counterfactuals", "Any knowledge that we have of what is going on in them is parasitic on our knowledge of counterfactual truths."),
    ("Other worlds have nothing to do with counterfactual truth.", "Counterfactuals", "other worlds have nothing to do with counterfactual truth."),
    ("Lewis' analysis (LA) is false.", "Lewis", "Which shows that LA is false."),
    ("Statements about the past confirm statements about the future.", "Induction", "I believe that statements about the past confirm statements about the future."),
    ("It is hard to reconcile confirmation with Humeanism.", "Hume", "It is hard to reconcile this belief with Humeanism."),
    ("Lewis' analysis (LA) is clever but false.", "Lewis", "LA is obviously a clever analysis. But it's false, and it's clear why."),
    ("Knowledge of other worlds is based on knowledge of our own world.", "Lewis", "any knowledge that we have of what happens after t in other worlds will be based on our knowledge of what happens after t in our world."),
    ("LA assumes knowledge of our own world's future, which is question-begging.", "Lewis", "So LA goes through only if it's assumed, question-beggingly, that we know what will happen in our own world's future."),
    ("The unknown cannot be assumed to resemble the known without question-begging.", "Induction", "Given only that such and such is true of the known, it can't be assumed that it also holds of the unknown—unless it's assumed, question-beggingly, that the unknown resembles the known."),
    ("LA assumes that inductive inference works, which is question-begging.", "Induction", "So LA goes through only if it's assumed, question-beggingly, that inductive inference works."),
    ("There is no knowledge without certainty.", "Epistemology", "In general, there's no knowledge where there isn't certainty."),
    ("If there is any chance that P isn't the case, then you don't know P.", "Epistemology", "If, given the information at your disposal, there is any chance, no matter how small, that P isn't the case, then you don't know P."),
    ("The merely probable is not known.", "Epistemology", "The merely probable is ipso facto not known."),
    ("To know something is 99.9999% likely is to not know it.", "Epistemology", "To know it to be 99.9999% likely that unsupported objects will continue to fall is to not know that they'll fall."),
    ("Statistical improbability is innocuous.", "Probability", "Statistical improbability is innocuous."),
    ("It's explanatory improbability that you have to worry about.", "Probability", "It's explanatory improbability that you have to worry about."),
    ("Every event is improbable in the statistical sense.", "Probability", "Every event is improbable in the statistical sense."),
    ("Winning the lottery is improbable in the statistical sense but not in the explanatory sense.", "Probability", "My winning the lottery is improbable in the statistical sense, but not in the explanatory sense."),
    ("Something is grue if it is green before Jan. 1, 2010, or blue thereafter.", "Grue Paradox", "Something is grue if it is green before Jan. 1, 2010, or blue thereafter."),
    ("All emeralds examined before 2010 are grue.", "Grue Paradox", "the fact that all emeralds examined before 2010 are green means that all emeralds examined before 2010 are grue."),
    ("The degree to which a fact is statistically improbable depends on how it is described.", "Probability", "The degree to which a given fact is statistically improbable depends on how it is described."),
    ("The supposition that objects don't change color is deeply embedded in scientific theory.", "Grue Paradox", "The supposition that objects don't change color is deeply embedded in scientific theory and also in the commonsense underpinning of scientific theory."),
    ("If the supposition that objects don't change color is wrong, then science is in serious trouble.", "Grue Paradox", "If it's wrong, then science is in serious trouble, and so is human knowledge in general."),
    ("Natural selection preserves structures that accurately represent the world.", "Evolution", "Natural selection preserves those cognitive structures that accurately represent the world."),
    ("Our hardwired belief in universal causation was selected for because it's true.", "Evolution", "our hardwired belief in universal causation was selected for because it's true."),
    ("Inborn expectations about uniform causal regularities presuppose those very regularities.", "Induction", "inborn expectations about uniform causal regularities presuppose the very regularities that we're using those expectations to explain."),
    ("Probability judgments are rational when they merely redescribe statistics.", "Probability", "Probability judgments are rational when they merely redescribe statistics"),
    ("Probability judgments are irrational within a Humean framework when they involve extrapolations.", "Probability", "Probability judgments are irrational, given a Humean framework, when they involve extrapolations."),
    ("De facto generalizations don't receive support from their instances.", "Confirmation", "de facto generalizations don't receive support from their instances"),
    ("Accidental generalizations do not receive support from their instances.", "Confirmation", "accidental generalizations don't receive support from their instances"),
    ("For Hempel's paradox to arise, at least one statement must be taken as more than a de facto concomitance.", "Hempel's Paradox", "if Hempel's paradox is to arise, at least one of MH and NH must be taken as doing more than affirming a de facto concomitance"),
    ("Hempel's paradox does not arise if HM has no nomic content.", "Hempel's Paradox", "Hempel's paradox doesn't arise if we don't take HM to have nomic content."),
    ("A nomic connection between having phi and psi does not imply a nomic connection between not having psi and not having phi.", "Nomic Relations", "Given only that there is a nomic connection between a thing's having phi and its having psi, it doesn't follow that there is a nomic connection between a thing's not having psi and its not having phi"),
    ("Nomic relations hold only among occupants of the space-time manifold.", "Nomic Relations", "it is pretty clear they hold only among occupants of the space-time manifold."),
    ("Nomic relations hold among events.", "Nomic Relations", "They clearly hold among events (my pounding the table causes it to break)."),
    ("Nothing non-spatiotemporal stands in nomic relations.", "Nomic Relations", "it is clear that nothing non-spatiotemporal stands in them."),
    ("Seeing a million black ravens does not guarantee the next raven will be black without a causal connection.", "Confirmation", "Maybe you've seen a million ravens, all of them black. It doesn't matter. Unless you have reason to believe that a thing's being a raven is connected somehow to its being black"),
    ("A black raven can only support 'All ravens are black' if there is a causal or nomic connection between ravenhood and blackness.", "Confirmation", "If the existence of a black is raven is to provide any legitimate support for (1), there must be a causal or nomic connection between ravenhood and blackness."),
    ("When read as affirming de facto concomitances, MH and HM are confirmationally identical.", "Confirmation", "If read as doing nothing more than affirming de facto concomitances: (MH) and (HM) don't receive support from their instances and are therefore vacuously confirmationally identical."),
    ("When read as alleging nomic connections, MH and HM are not logically equivalent.", "Confirmation", "If they are read as alleging some kind of nomic connection, they don't even appear logically equivalent."),
    ("Hume's argument concerning induction would invalidate certain arguments about knowledge.", "Induction", "If Hume's argument concerning induction goes through, then the following argument fails to go through"),
    ("According to the counterfactual analysis of causation, if the cause hadn't occurred, the effect wouldn't have occurred.", "Counterfactuals", "if the cause of the doorbell's ringing is the button's being pushed, then the doorbell wouldn't have rung if the button hadn't been pushed."),
    ("If AC is right, then causal connections are not known empirically but through logical analysis.", "Causation", "If AC is right, then causal connections are not to be known empirically, and must instead be known through logical analysis."),
    ("If AC is right, we can't see or otherwise sense-perceive causal connections.", "Causation", "If AC is right, then we can't see, or otherwise sense-perceive, causal connections."),
    ("The only way to know that E1 caused E2 is to know of some general regularity.", "Causation", "The only way to know that E1 caused E2 is to know of some general regularity of which the sequence of events consisting of E1 and E2 is an instance."),
    ("There is a problem with Hume's analysis of causality due to causal redundancy.", "Causation", "One problem with the analysis of causality is that, because there is a certain amount of causal redundancy in the world, there are cases where a given event would have occurred even if the event that in fact caused it had not happened."),
    ("A miracle is needed to validate counterfactuals according to Lewis.", "Lewis", "Lewis is saying that, if a world validates LASK, there is some miracle in it."),
    ("A theory supported only by doctored data is a bad theory.", "Methodology", "A theory that only doctored data supports is a bad theory, and Lewis' analysis of counterfactuals is untenable."),
    ("Smith's falling off of a building is an event that causes other events.", "Causation", "Smith's falling off of X is an event. It is something that makes things happen."),
    ("Brown's not falling off a building is not an event.", "Causation", "Whereas Smith's falling off of X is an event, Brown's not falling off of X is not an event,"),
    ("Brown's not falling off a building is not constituted by events.", "Causation", "Brown's not falling off of X isn't identical with an event and isn't constituted by events."),
    ("A chair consists of events (various miniscule displacements of mass-energy).", "Causation", "A chair consists of events (various miniscule displacements of mass-energy),"),
    ("A corporation consists of events (various actions on the part of sentient beings).", "Causation", "and does a corporation (various actions on the part of sentient beings);"),
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
    
    for pos_text, topic, quote in analytic_positions:
        pos_id = f"AP-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"AP-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Chapter 17: Analytic Philosophy - J.-M. Kuczynski",
            "work_id": "WORK-ANALYTIC-PHIL",
            "domain": "analytic_philosophy"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Chapter 17 Analytic Philosophy: +{len(new_positions)} positions with quotes"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 20,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Chapter 17: Analytic Philosophy",
            "positions": len(new_positions),
            "topics": ["Causation", "Hume", "Lewis", "Counterfactuals", "Functionalism", "Content-Externalism", "Confirmation", "Grue Paradox", "Hempel's Paradox", "Induction", "Probability", "Nomic Relations"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Analytic Philosophy (Ch17) positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: AP-{max_ap_num+1:03d} to AP-{counter-1:03d}")

if __name__ == "__main__":
    main()
