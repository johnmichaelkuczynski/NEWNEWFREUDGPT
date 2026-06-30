#!/usr/bin/env python3
"""
Add Existentialism positions with quotes to the Kuczynski database.
"""

import json
from datetime import datetime

existentialism_positions = [
    ("Existentialism is more of an attitude than a doctrine.", "Existentialism", "At its core, existentialism is therefore less of a doctrine than it is an attitude."),
    ("A doctrine is a system of interconnected propositions.", "Existentialism", "A doctrine is a system of interconnected propositions."),
    ("The viability of a doctrine has nothing to do with how anyone feels about anything.", "Existentialism", "The viability of a doctrine has nothing to do with how anyone feels about anything."),
    ("Doctrines are to be judged according to logical or empirical benchmarks.", "Existentialism", "They are to be judged according to how well they measure up to the relevant logical or empirical benchmarks."),
    ("Attitudes cannot be judged as right or wrong.", "Existentialism", "Attitudes cannot be understood in these terms."),
    ("To the extent that it is an attitude, existentialism cannot be judged to be wrong.", "Existentialism", "So to the extent that it is an attitude, existentialism cannot be judged to be wrong."),
    ("Choosing values leads to more reflection on what values should be.", "Existentialism", "If you come into the world believing that values are to be chosen, as opposed to passively accepted, you are probably more likely than you would otherwise be to reflect on what your values should be."),
    ("Choosing values is psychologically beneficial.", "Existentialism", "First, if you choose your values, instead of simply accepting the values of others, you are more likely to live according to values that work for you psychologically."),
    ("Even choosing the wrong values affirms rationality and freedom.", "Existentialism", "Second, even if you choose the wrong values, the mere fact that you chose your values would seem to be an affirmation of your rationality and freedom."),
    ("Some values involve a diminishment of self.", "Existentialism", "A number of values seem to involve a diminishment of self."),
    ("Society's values are good for society but not necessarily for the individual.", "Existentialism", "One possible answer is that the values that are endorsed by society are those that are good for society, and therefore aren't necessarily those that are good for the individual."),
    ("Society requires the abridgment of individual freedoms.", "Existentialism", "As Freud emphasized in Civilization and its Discontents, society is possible only if the aspirations of individuals are abridged."),
    ("Society's values embody much of the antagonism people have for one another.", "Existentialism", "the values that society asks the individual to accept embody much of the antagonism that people have for one another."),
    ("Choosing values protects against moralistic propaganda.", "Existentialism", "If you see values as yours to accept or reject, you are less likely to be duped by moralistic propaganda into reducing yourself."),
    ("Existentialist philosophers have produced doctrines to validate the existentialist attitude.", "Existentialism", "existentialist philosophers have spent a great deal of time producing doctrines that validate the attitude in question."),
    ("The doctrines produced by existentialist philosophers may not be correct or coherent.", "Existentialism", "Even though that attitude may be salutary, it doesn't follow that those doctrines are correct or even coherent."),
    ("The values other people tell us to accept may not always be the right ones.", "Ethics", "The values that other people tell us to accept may not always be the right ones."),
    ("It doesn't follow that there are no values.", "Ethics", "But it doesn't follow that there are no values"),
    ("Rejecting conventional values can be to uphold other values.", "Ethics", "Sometimes when people reject conventional values, it is because they feel that they must do so to uphold other values."),
    ("Fruitful rebellion against conventional values involves acceptance of deeper values.", "Ethics", "It would be hard to think of a single case where a fruitful rebellion against conventional values did not involve an acceptance of a deeper and more legitimate set of values."),
    ("Attitudes are not themselves true or false.", "Existentialism", "We said earlier that attitudes are not themselves true or false."),
    ("Attitudes involve presuppositions that are true or false.", "Existentialism", "But, despite this fact, attitudes often involve presuppositions that are true or false."),
    ("Emotional attitudes are grounded in beliefs about the world.", "Existentialism", "In general, our emotional attitudes are grounded in beliefs about the world, and those beliefs are true or false."),
    ("The thesis that there are no universally valid moral truths is controversial.", "Ethics", "there are no universally valid moral truths."),
    ("Feelings can have an objective basis.", "Ethics", "MR presupposes that feelings cannot possibly have any objective basis. But this isn't so."),
    ("Our feelings track our feelings about rightness and wrongness.", "Ethics", "Our feelings seem to track our feelings about rightness and wrongness."),
    ("Our feelings are not always appropriate.", "Ethics", "This is not to say that our feelings are always appropriate."),
    ("It doesn't follow that feelings are categorically without an objective basis.", "Ethics", "it doesn't follow that they are categorically without an objective basis."),
    ("Our perceptions aren't always completely accurate, but that doesn't mean they're always wrong.", "Epistemology", "Our perceptions aren't always completely accurate. But that doesn't mean that they are always completely wrong."),
    ("There is a strong pre-theoretic presumption that there are objective moral truths.", "Ethics", "there is a strong pre-theoretic presumption to the effect that there are objective moral truths."),
    ("The word 'value' is ambiguous with at least three meanings.", "Ethics", "the word 'value' is ambiguous as it has (at least) three meanings."),
    ("A 'value' can be something valued or something one ought to value.", "Ethics", "A 'value' can be something that is in fact valued, or it can be something that one ought to value."),
    ("Moral truths would not be false in a world of sociopaths.", "Ethics", "In a world of mathematical morons, nobody would know that 2 + 2 = 4; but the statement '2 + 2 = 4' would not on that account be false."),
    ("People often come to believe they have been abiding by the wrong values.", "Ethics", "People often come to believe that they have been abiding by the wrong values, and must therefore adopt new ones."),
    ("Tolstoy's The Death of Ivan Ilyich illustrates the point about changing values.", "Ethics", "Tolstoy's novel The Death of Ivan Ilyich illustrates this point."),
    ("Emotions track value-judgments.", "Ethics", "In general, it's hard to believe that emotions don't track value-judgments."),
    ("Emotions embody value-judgments.", "Ethics", "Supposing that our emotions embody value-judgments, it seems to follow that we cannot choose any value-system without jeopardizing our own happiness."),
    ("Emotions presuppose certain ethical views.", "Ethics", "It thus seems that your emotions presuppose certain ethical views."),
    ("Changing value system requires changing emotions.", "Ethics", "a necessary condition for really accepting a new set of values would be that you re-wire, so to speak, your emotions."),
    ("Innate psychological structure limits happiness.", "Ethics", "Your innate psychological structure obviously puts limits on what you can do and still be happy."),
    ("Emotional state tracks views on moral fitness.", "Ethics", "Your emotional state tracks your views as to the moral fitness of facts about your life."),
    ("Certain value systems are internal to emotional architecture.", "Ethics", "certain value systems are internal to his/her emotional architecture."),
    ("The range of admissible value systems is limited by psychology and biology.", "Ethics", "the range of admissible value systems is limited by immutable facts about our psychology (and biology)."),
    ("Chomsky showed humanly learnable languages satisfy narrowly defined formal constraints.", "Linguistics", "Chomsky showed that any humanly learnable language satisfies rather narrowly defined formal constraints."),
    ("One cannot change value system except in trivial respects.", "Ethics", "you cannot (except in trivial respects) change your value system at all."),
    ("One can comply with a value system that doesn't make one happy.", "Ethics", "Of course, you can, in terms of your overt behavior, comply with a value system that doesn't make you happy."),
    ("True acceptance of a value system requires emotional alignment.", "Ethics", "But if the view we've been defending is right, you don't really accept such a value system."),
    ("Emotions reflect actual values.", "Ethics", "If your emotions reflect your actual values, then you don't really accept a value system that brings you misery."),
    ("Choosing one's own ethics may embody a contradiction.", "Ethics", "Does it make sense to say that it is ethically permissible to choose one's own ethics? Doesn't that question embody a contradiction?"),
    ("If there is no God, there are no moral laws.", "Ethics", "In other words, if there is no God, there are no moral laws."),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_ex_num = 0
    for pid in existing_ids:
        if pid.startswith('EX-'):
            try:
                num = int(pid.split('-')[1])
                max_ex_num = max(max_ex_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_ex_num + 1
    
    for pos_text, topic, quote in existentialism_positions:
        pos_id = f"EX-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"EX-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Existentialism - J.-M. Kuczynski",
            "work_id": "WORK-EXISTENTIALISM",
            "domain": "existentialism"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Existentialism: +{len(new_positions)} positions with quotes"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 21,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Existentialism",
            "positions": len(new_positions),
            "topics": ["Existentialism", "Ethics", "Values", "Emotions", "Psychology"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Existentialism positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: EX-{max_ex_num+1:03d} to EX-{counter-1:03d}")

if __name__ == "__main__":
    main()
