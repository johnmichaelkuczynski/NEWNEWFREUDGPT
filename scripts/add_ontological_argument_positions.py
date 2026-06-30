#!/usr/bin/env python3
"""
Add Ontological Argument positions with quotes to the Kuczynski database.
"""

import json
from datetime import datetime

ontological_positions = [
    ("The Ontological Argument (AG) is a spurious argument.", "Ontological Argument", "AG is a spurious argument."),
    ("God does not exist in the mind—if God exists, She is in the world.", "Ontological Argument", "If God exists, She is out there, in the world, not in my mind."),
    ("No idea of mine is God.", "Ontological Argument", "No idea of mine is God."),
    ("The only things that exist in the mind are thoughts, feelings, etc.", "Ontological Argument", "The only things that exist in my mind are thoughts, feelings, etc."),
    ("A representation of the Sun existing in the mind doesn't entail the Sun exists in the mind.", "Ontological Argument", "But the fact that a representation of the Sun exists in my mind obviously doesn't entail that the Sun itself exists in my mind."),
    ("Having knowledge of what conditions a thing must fulfill does not imply its existence.", "Ontological Argument", "But given only that I have this knowledge, it doesn't follow that there exists anything that has any of the requisite properties."),
    ("God is a maximally excellent thing by definition.", "Ontological Argument", "Just as squares are, by definition, four-sided, so God is, by definition, maximally excellent."),
    ("If an object is deficient in any way, it fails to be God.", "Ontological Argument", "If we found that object X was deficient in some way—that it was ill-willed or stupid or lazy—then it would, for that very reason, fail to be God."),
    ("Existence is an excellence.", "Ontological Argument", "Existence is an excellence."),
    ("Failing to exist is the worst kind of failure.", "Ontological Argument", "But no failure is as bad as the failure to exist."),
    ("If you don't exist, you are a complete and total zero.", "Ontological Argument", "If you don't exist, you are a nothing, a complete and total zero."),
    ("The ontological argument appears to beg the question.", "Ontological Argument", "But the ontological argument appears to do just this."),
    ("Step 1 of the ontological argument is just another way of saying God exists.", "Ontological Argument", "Step 1 is just another way of saying: There exists a certain thing, namely God, which is maximally excellent."),
    ("The ontological argument fails to prove God's existence if it assumes God exists.", "Ontological Argument", "But if Steps 1 and 2 are taken in this way, then the argument question-beggingly assumes that God exists."),
    ("If God exists, then She has every excellence, including existence.", "Ontological Argument", "What follows from these three statements is that: If God exists, then He has every excellence, including existence."),
    ("'If God exists, She exists' is all the ontological argument proves.", "Ontological Argument", "In other words, if God exists, She exists."),
    ("The ontological argument proves nothing.", "Ontological Argument", "So the ontological argument proves nothing."),
    ("SOA presupposes that failing to exist makes a thing imperfect.", "Ontological Argument", "SOA presupposes that a given thing's failing to exist makes it imperfect."),
    ("It's incoherent to say that failing to exist makes you a lesser person.", "Ontological Argument", "But it's incoherent. If you didn't exist, you wouldn't be a lesser person."),
    ("If you didn't exist, there would be no you to begin with.", "Ontological Argument", "If you didn't exist, you wouldn't be a lesser person. There would be no you to begin with."),
    ("It is not possible for something to fail to exist.", "Ontological Argument", "For there to be something that failed to exist would be for there to exist something x such that x did not exist. And that, clearly, is not possible."),
    ("'Square circles don't exist' means no object can be both a square and a circle.", "Logic", "Rather, SC says that any given thing is a non-square if it's a circle."),
    ("'Zeus doesn't exist' means no object has the properties attributed to Zeus.", "Logic", "ZE makes the innocuous claim that given any object x, x doesn't have the property of being a unique, lightning-bolt hurling god."),
    ("Statements about non-existence attribute properties to properties, not non-existence to objects.", "Logic", "Thus, SC and ZE attribute properties to properties. They don't attribute non-existence to objects."),
    ("It is not possible to attribute non-existence to a non-existent object.", "Logic", "It isn't even possible to attribute non-existence to a non-existent object."),
    ("It is not possible to attribute existence to a non-existent object.", "Logic", "Nor is it possible to attribute existence to a non-existent object."),
    ("A precondition for a thing's being described as existent or non-existent is its existing.", "Logic", "It follows that a precondition for a thing's being described as existent or non-existent is its existing."),
    ("In attributing existence to a given thing, one isn't affirming anything.", "Logic", "Since any given proposition can be negated, it follows that, in attributing existence to a given thing, one isn't affirming anything."),
    ("It is meaningless to say of specific individuals that they exist or don't exist.", "Logic", "It is meaningless to say of specific individuals that they exist or don't exist."),
    ("Claiming ethical judgments are by-products of upbringing denies their objectivity.", "Ethics", "if you say that our ethical judgments are by-products of our upbringing, and therefore aren't hewed to anything objective"),
    ("Denying the objectivity of ethical judgments undermines one's right to assert any judgments.", "Ethics", "then you are ipso facto denying that your judgments are any good, in which case you forfeit your right to assert anything"),
    ("St. Thomas Aquinas argued against DCT.", "Ethics", "St. Thomas Aquinas argues against DCT"),
    ("Since Aquinas' time, it has been heresy in the Catholic Church to accept DCT.", "Ethics", "Since Aquinas' time, it has been heresy in the Catholic Church to accept DCT"),
    ("To the extent Aquinas rejected DCT, he wasn't religious.", "Philosophy of Religion", "My feeling is that to the extent that Aquinas rejected DCT, he wasn't religious"),
    ("To the extent Aquinas was religious, he actually did accept DCT.", "Philosophy of Religion", "to the extent that he was religious, he actually did accept DCT"),
    ("Religious intellectuals are masters of compartmentalization.", "Philosophy of Religion", "Religious intellectuals are masters of compartmentalization"),
    ("Free will theodicy presupposes there is such a thing as free will.", "Theodicy", "One of the two theodicies that we discussed presupposes that there is such a thing as free will"),
    ("It is questionable whether there is such a thing as free will.", "Free Will", "Then say why it is questionable whether there is such a thing as free will"),
    ("Even if there is free will, it wouldn't necessarily help the theodicy.", "Theodicy", "Also say why, supposing that there is free will, it wouldn't necessarily help the theodicy in question"),
    ("God is omniscient.", "Philosophy of Religion", "According to many, God is omniscient"),
    ("God's omniscience implies knowledge of all actions of every person.", "Philosophy of Religion", "Given that God is omniscient, He/She has always known exactly what each person would do at each moment of his/her life"),
    ("God's omniscience could imply a lack of free will.", "Free Will", "Does this mean that you have no free will?"),
    ("The free-will theodicy presupposes God's omniscience and knowledge of the future.", "Theodicy", "The free-will theodicy presupposes that God is omniscient and therefore knows exactly what the future holds"),
    ("God's knowledge of future actions challenges the concept of free will.", "Free Will", "But if Gods knows now what I will do 10 years from now, it's hard to see how I could possibly have any free will"),
    ("The Free Will defense leads to the paradox of both having and not having free will.", "Theodicy", "The Free Will defense thus seems to have the absurd consequence that people both do, and do not, have free will"),
    ("Descartes believed an omnipotent God can make 1 + 1 = 3.", "Omnipotence", "According to Descartes, God, being omnipotent, can make 1 + 1 = 3"),
    ("Wittgenstein believed even an omnipotent God cannot make 1 + 1 = 3.", "Omnipotence", "According to Wittgenstein, even if God is omnipotent, He/She cannot make 1 + 1 = 3"),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_pr_num = 0
    for pid in existing_ids:
        if pid.startswith('PR-'):
            try:
                num = int(pid.split('-')[1])
                max_pr_num = max(max_pr_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_pr_num + 1
    
    for pos_text, topic, quote in ontological_positions:
        pos_id = f"PR-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"PR-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Philosophy of Religion - J.-M. Kuczynski",
            "work_id": "WORK-PHIL-RELIGION",
            "domain": "philosophy_of_religion"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Ontological Argument: +{len(new_positions)} positions with quotes"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 23,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Ontological Argument",
            "positions": len(new_positions),
            "topics": ["Ontological Argument", "Logic", "Theodicy", "Free Will", "Omnipotence"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Ontological Argument positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: PR-{max_pr_num+1:03d} to PR-{counter-1:03d}")

if __name__ == "__main__":
    main()
