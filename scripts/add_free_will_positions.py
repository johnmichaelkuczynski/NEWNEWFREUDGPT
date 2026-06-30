#!/usr/bin/env python3
"""
Add Free Will and Compatibilism positions with quotes to the Kuczynski database.
"""

import json
from datetime import datetime

free_will_positions = [
    ("The physical world is a deterministic system.", "Determinism", "The physical world is a deterministic system."),
    ("There are both physical and mental entities.", "Mind-Body Problem", "There are both physical and mental entities."),
    ("Anything that involves thought or feeling is mental; anything that does not but is spatiotemporal is physical.", "Mind-Body Problem", "Anything that involves thought or feeling is mental; anything that does not (but is spatiotemporal) is physical."),
    ("Beliefs, intentions, and regrets are mental; rocks, trees, and explosions are physical.", "Mind-Body Problem", "So beliefs, intentions, and regrets are mental; and rocks, trees, and explosions are physical."),
    ("It is an open and delicate question how the mental and physical are related.", "Mind-Body Problem", "It is an open and delicate question how the mental and physical are related."),
    ("Materialism is the position that mental entities are identical with certain physical entities.", "Materialism", "Some hold that mental entities are identical with certain physical entities... This position is known as materialism."),
    ("Dualism is the position that the mental is non-physical.", "Dualism", "Others deny this, saying that the mental is non-physical. This position is known as dualism."),
    ("If materialism is right, then the mental world is just part of the physical world.", "Materialism", "If materialism is right, then the mental world is just part of the physical world."),
    ("Given the way the world was 10 million years ago, the state of the universe made any experience's occurrence inevitable.", "Determinism", "So if E is some experience that you either have had, are having, or will have, then given the way the world was 10 million years ago, the state of the universe 10 million years ago made E's occurrence inevitable."),
    ("Whatever you decide to do today is an inevitable consequence of the way the world was a million years ago.", "Determinism", "Whatever you decide to do today is an inevitable consequence of the way the world was a million years ago."),
    ("Supposing that the physical world is deterministic and materialism is right, it's hard to see how there could be free will.", "Free Will Problem", "Supposing that the physical world is deterministic, and supposing also that materialism is right, it's hard to see how there could be free will."),
    ("If the state of the universe a million years ago completely settled what choices I would make today, then I couldn't make any choices other than those that I do make.", "Free Will Problem", "If the state of the universe a million years ago completely settled what choices I would make today, then presumably I couldn't make any choices other than those that I do make."),
    ("Some believers in free will accept dualism because of the apparent irreconcilability of materialism with the presumption that we are free.", "Dualism", "Because of the apparent irreconcilability of materialism with the presumption that we are free, some believers in free will—for example, Jean Paul Sartre and Maurice Merleau-Ponty—accept dualism."),
    ("Others accept materialism but reject determinism.", "Free Will Problem", "while others, e.g. Peter van Inwagen, accept materialism but reject determinism."),
    ("Supposing that there is indeterminism in the world, it doesn't necessarily mean that our mental processes aren't determined.", "Indeterminism", "First of all, supposing that there is indeterminism in the world, it doesn't necessarily mean that our mental processes aren't determined."),
    ("There is some corroboration for the view that decisions are determined by unconscious forces.", "Determinism", "In any case, this is one point of view, and it is one for which there is some corroboration."),
    ("Choices not fixed by the state of the universe prior to their occurrence would not be free.", "Free Will Problem", "For the reasons given earlier, that wouldn't make those choices be free."),
    ("Choices not fixed by prior states of the universe would be more like fits or seizures than freely made judgments.", "Free Will Problem", "On the contrary, it would make them more like fits or seizures than like considered, freely made judgments."),
    ("A sudden choice to drop out of college and become a drug dealer does not sound like a freely made choice—it sounds more like a compulsion.", "Free Will Problem", "Does this sound like a freely made choice? No. It sounds more like a compulsion."),
    ("Indeterminism doesn't help freedom and actually undermines it.", "Indeterminism", "Again, we see that indeterminism doesn't help freedom and actually undermines it."),
    ("Determinism seems to threaten freedom.", "Free Will Problem", "The problem is that, as we saw, determinism also seems to threaten freedom."),
    ("If determinism is right, the past completely determines what choices you're making now.", "Determinism", "If determinism is right, then what happened in the past completely determines exactly what's happening in the present and, in particular, completely fixes what choices you're making now."),
    ("Under determinism, something over which you have no control is completely responsible for your choices.", "Determinism", "So something over which you have no control is completely responsible for the choices that you're making."),
    ("It's hard to see how you could have free will under determinism.", "Free Will Problem", "It's hard to see how, under these circumstances, you could be said to have free will."),
    ("Compatibilists believe there can be free will in a deterministic world.", "Compatibilism", "Some hold that there can be free will in a deterministic world. Such people are known as compatibilists."),
    ("Incompatibilists deny that there can be free will in a deterministic world.", "Incompatibilism", "Those who deny it are incompatibilists."),
    ("There are two different forms of compatibilism.", "Compatibilism", "There are ultimately two different forms of compatibilism."),
    ("According to the straightforward version of compatibilism, you are free to the extent that you can do what you want.", "Compatibilism", "According to the straightforward version, you are free to the extent that you can do what you want, and you are unfree to the extent that you cannot."),
    ("According to the other version of compatibilism, being able to do what you want is necessary but not sufficient for freedom.", "Compatibilism", "According to the other version of compatibilism, being able to do what you want, though necessary for freedom, isn't sufficient for it."),
    ("G.E. Moore believes an act is performed freely if the agent would have done something else if he had chosen to do so.", "Compatibilism", "According to G.E. Moore, an act is performed freely if the agent would have done something else if he had chosen to do so."),
    ("Free acts aren't those that are uncaused; they're those that are caused by decisions on the part of the people who commit them.", "Compatibilism", "Free acts aren't those that are uncaused; they're those that are caused in a certain way—they're those that are caused by decisions on the part of the people who commit them."),
    ("Chisholm objects to Moore's analysis: if every choice I make is inevitable, it's irrelevant that I would have acted differently had I made different choices.", "Free Will Problem", "If every choice I make is inevitable, then it's irrelevant that, had I made different choices, I would have acted differently."),
    ("Chisholm's point is a good one, but it isn't decisive.", "Free Will Problem", "Chisholm's point is a good one, but it isn't decisive."),
    ("Freedom is a property of actions, according to Locke.", "Compatibilism", "In Locke's view, freedom is a property of actions."),
    ("Only things that one can intend to do are done freely.", "Compatibilism", "Only things that one can intend to do are done freely."),
    ("Second-order intentions (intentions to intend) collapse into first-order intentions.", "Compatibilism", "Second-order intentions (intentions to intend) collapse into first-order intentions."),
    ("Choices can be made freely according to a defensible form of compatibilism.", "Compatibilism", "according to one, quite defensible form of compatibilism, choices can be made freely"),
    ("Freedom is primarily a property of choices and only secondarily of acts.", "Compatibilism", "freedom is primarily a property of choices and only secondarily of acts"),
    ("Harry Frankfurt decisively demonstrated the falsity of Moore's position.", "Frankfurt Cases", "Harry Frankfurt decisively demonstrated the falsity of Moore's position"),
    ("Somebody can perform an act freely even if they could not have abstained from performing that act.", "Frankfurt Cases", "scenarios in which somebody performs some act freely even though that person could not have abstained from performing that act"),
    ("'x performs act A freely' is not equivalent with 'x does A and, had x chosen not to do A, x would not have done A.'", "Frankfurt Cases", "'x performs act A freely' is not equivalent with 'x does A and, had x chosen not to do A, x would not have done A.'"),
    ("Moore's analysis is a misguided way of stating the principle that a free act is one that is choice-driven.", "Compatibilism", "it's really just a misguided way of stating the principle that a free act is one that is choice-driven"),
    ("The counterfactual analysis of causality is wrong.", "Causation", "CFA is wrong."),
    ("There is causal redundancy in the world.", "Causation", "This is because there is causal redundancy in the world."),
    ("Counterfactuals typically have to be hedged with ceteris paribus clauses to come out correct.", "Counterfactuals", "It's well known that, if they are to come out correct, counterfactuals typically have to be hedged with ceteris paribus clauses."),
    ("As a rule, counterfactuals are causal claims.", "Counterfactuals", "As a rule, counterfactuals are causal claims."),
    ("An act is free if it expresses one's decision to act that way.", "Compatibilism", "an act is free if it expresses one's decision to act that way."),
    ("One chooses to act; one doesn't choose to choose.", "Compatibilism", "One chooses to act, Locke said; one doesn't choose to choose."),
    ("It makes no sense to suppose that one chooses to choose.", "Compatibilism", "It makes no sense to suppose that one chooses to choose."),
    ("One would have to make infinitely many choices to make a single choice if one always chose what to choose.", "Compatibilism", "For if one always chose what to choose, Locke points out, one would have to make infinitely many choices in order to make a single one"),
    ("Freedom is freedom to act, not freedom to choose.", "Compatibilism", "So freedom is freedom to act, not freedom to choose."),
    ("Freedom is a relationship between choice and act, not between subject and choice.", "Compatibilism", "freedom is a relationship between choice and act, and not between subject and choice."),
    ("It is irrelevant whether one's choices are caused or not, so far as one's freedom is concerned.", "Compatibilism", "so far as one's freedom is concerned, it is irrelevant whether one's choices are caused or not."),
    ("It doesn't matter whether choices are caused for freedom, nor how they're caused.", "Compatibilism", "it doesn't matter whether choices are caused... Nor does it matter how they're caused"),
    ("Determinism is not only compatible with freedom but is a prerequisite for it.", "Compatibilism", "if FA is right, determinism is not only compatible with freedom but is a prerequisite for it"),
    ("Indeterministic mechanisms can undermine the implementation of choices.", "Indeterminism", "If a degenerative neurological condition has undermined the integrity of the mechanisms linking your brain to your hand, thereby making them indeterministic, your intention to move your hand may be more likely to fail than to succeed"),
    ("To the extent that the mechanisms involved in the implementation of our choices are indeterministic, we are in the position of somebody who has Parkinson's.", "Indeterminism", "To the extent that the mechanisms involved in the implementation of our choices are indeterministic, we are in the grim position of somebody who has Parkinson's"),
    ("There are different kinds of freedom.", "Free Will Problem", "This is obviously a kind of freedom—a very important kind. But it isn't the only kind"),
    ("Contrary to what Locke says, there is a sense in which choices can be free or unfree.", "Free Will Problem", "And, contrary to what Locke says, there is a sense in which choices can be free or unfree"),
    ("A person can have conflicting desires.", "Frankfurt Cases", "He thus has a desire to not take the heroin—even though he simultaneously has a desire to take the heroin"),
    ("A first-order desire is a desire to do something.", "Frankfurt Cases", "Jones' desire to take heroin is a first-order desire"),
    ("A second-order desire is a desire about another desire.", "Frankfurt Cases", "Jones' desire not to take heroin is a desire as to what to do with another desire; it is a desire not to cave in to a desire to take heroin"),
    ("Free will is aligned with second-order desires.", "Frankfurt Cases", "Frankfurt says that somebody has a free will to the extent that his conduct aligns with his second-order desires"),
    ("Rationality drives the decision not to act on a first-order desire.", "Frankfurt Cases", "When the heroin-addicted writer decides not to take heroin, what is driving him is a rational appraisal of his situation"),
    ("Self-consciousness is a key feature of persons.", "Personhood", "First of all, we are self-conscious"),
    ("Rationality is a key feature of persons.", "Personhood", "Second, we are rational"),
    ("Persons are rational not only about how to attain their objectives, but also about what those objectives should be.", "Personhood", "Third, we are rational not only about how to attain our objectives, but also about what those objectives should be"),
    ("What distinguishes persons from non-persons is that persons subject their own desires to critical scrutiny.", "Personhood", "What distinguishes persons from non-persons is that the former, but not the latter, subject their own desires to critical scrutiny"),
    ("Self-consciousness enables rational assessment of desires.", "Personhood", "And this is obviously made possible by the fact that we are self-conscious"),
    ("Whenever someone is driven by a rational assessment of their own desires, they are driven by a desire about a desire.", "Frankfurt Cases", "Whenever someone is driven by a rational assessment of their own desires, they are driven by a desire about a desire"),
    ("There is a clear sense in which rational conduct is free and irrational conduct is not.", "Free Will Problem", "There is a clear sense in which rational conduct is free and in which irrational conduct is not"),
    ("Your desires must reflect who you are. If they don't, those desires belong to you but aren't of you.", "Frankfurt Cases", "Your desires must reflect who you are. If they don't, those desires belong to you but aren't of you."),
    ("Alienation from one's desires is worse than alienation from one's body.", "Frankfurt Cases", "And in that case, you are alienated from your own mental states, in much the way that a person with Parkinson's is alienated from his body. But, in a way, the alienation is even worse."),
    ("Involuntary behavior is unintentional behavior.", "Action Theory", "Involuntary behavior is unintentional behavior."),
    ("Intentional behavior is voluntary behavior.", "Action Theory", "Intentional behavior is voluntary behavior."),
    ("Voluntary behavior is desire-driven behavior.", "Action Theory", "Voluntary behavior is desire-driven behavior."),
    ("Epileptic fits are not actions.", "Action Theory", "Epileptic fits are not actions."),
    ("Estrangement from one's actions leads to a lack of freedom.", "Free Will Problem", "So estrangement from one's own actions amounts to estrangement from all of one's actions; and it's hard to imagine a condition less free than that."),
    ("Freedom requires acting on second-order desires and alignment with first-order desires.", "Frankfurt Cases", "Thus, one is free insofar as two conditions are met: (i) one acts on one's second-order desires, as opposed to one's first-order desires; and (ii) one's second-order desires are in alignment with one's first-order desires."),
    ("All freedom might ultimately be about doing what one wants.", "Free Will Problem", "But, despite everything said thus far, a case can be made that at the end of the day all freedom is freedom to do what one wants."),
    ("Desires are structures, not feelings.", "Philosophy of Mind", "Desires, even short-lived ones, are structures; they aren't feelings."),
    ("The feelings to which a desire gives rise don't necessarily make it clear how intense that desire really is.", "Philosophy of Mind", "And the feelings to which a desire gives rise don't necessarily make it clear how intense that desire really is."),
    ("Many desires are rooted in personality structures.", "Philosophy of Mind", "Many desires are rooted in personality structures."),
    ("Addiction doesn't turn people into complete vegetables, at least not right away.", "Philosophy of Mind", "Addiction doesn't turn people into complete vegetables, at least not right away, and usually not ever."),
    ("Being free consists primarily in being oneself and secondarily in being able to do what one wants.", "Free Will Problem", "So being free consists primarily in being oneself and secondarily in being able to do what one wants."),
    ("To have a free will is to be free to decide what you want. It is not to be free to have what you want.", "Free Will Problem", "To have a free will is to be free to decide what you want. It is not to be free to have what you want."),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_fw_num = 0
    for pid in existing_ids:
        if pid.startswith('FW-'):
            try:
                num = int(pid.split('-')[1])
                max_fw_num = max(max_fw_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_fw_num + 1
    
    for pos_text, topic, quote in free_will_positions:
        pos_id = f"FW-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"FW-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Free Will and Compatibilism - J.-M. Kuczynski",
            "work_id": "WORK-FREE-WILL",
            "domain": "philosophy_of_mind"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Free Will and Compatibilism: +{len(new_positions)} positions with quotes"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 19,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Free Will and Compatibilism",
            "positions": len(new_positions),
            "topics": ["Free Will", "Compatibilism", "Frankfurt Cases", "Determinism", "Mind-Body Problem"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Free Will positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: FW-{max_fw_num+1:03d} to FW-{counter-1:03d}")

if __name__ == "__main__":
    main()
