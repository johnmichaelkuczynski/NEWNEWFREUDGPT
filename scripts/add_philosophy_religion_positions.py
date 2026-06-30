#!/usr/bin/env python3
"""
Add Philosophy of Religion positions with quotes to the Kuczynski database.
"""

import json
from datetime import datetime

religion_positions = [
    ("The so-called philosophy of religion doesn't concern religion itself.", "Philosophy of Religion", "The so-called philosophy of religion doesn't concern religion."),
    ("Philosophy of religion concerns logical puzzles, not religion.", "Philosophy of Religion", "It concerns puzzles that can be illustrated in connection with religious questions but are really of a strictly logical nature."),
    ("The Omnipotence Paradox is about logical subtleties, not God.", "Philosophy of Religion", "OG doesn't have anything to do with God. It has to do with subtleties of logic."),
    ("Philosophy of religion often veers off into irrelevant logical minutiae.", "Philosophy of Religion", "its efforts to do this quickly veer off course and end up bogging down in logical minutiae that are of no relevance to religion at all."),
    ("St. Thomas Aquinas's argument (AG1) is flawed.", "Philosophy of Religion", "So Aquinas has simply assumed that there was a first event, and he thus hasn't established it at all."),
    ("The first sentence of AG1 is ambiguous.", "Philosophy of Religion", "The first sentence of AG1, which we'll refer to as (a), is ambiguous."),
    ("Assuming a first event does not prove God's existence.", "Philosophy of Religion", "But supposing, if only for argument's sake, that there was a first event, it doesn't follow, at least not for any obvious reason, that it was an act of God."),
    ("Aquinas's second argument (AG2) for God's existence is flawed.", "Philosophy of Religion", "AG2 is a failure."),
    ("Comparatives do not require absolutes.", "Philosophy of Religion", "Contrary to what Aquinas believes, there don't have to be absolutes for there to be comparatives."),
    ("Pre-modern philosophers were only dimly aware of syntactic ambiguity.", "Philosophy of Religion", "Pre-modern philosophers, such as Aquinas, were only dimly aware of the phenomenon of syntactic ambiguity."),
    ("Studying Aquinas's arguments does not teach about God or religion.", "Philosophy of Religion", "But we didn't learn anything about God or religion."),
    ("It is futile to provide rational arguments for or against religious belief.", "Philosophy of Religion", "The futility of trying to provide rational arguments for or against religious belief"),
    ("Religion is not science or logic.", "Philosophy of Religion", "Religion is not science or logic."),
    ("A scientifically minded person's belief in God is contingent on available evidence.", "Philosophy of Religion", "Smith's belief in God goes only as far as the available evidence permits."),
    ("A person who believes in God isn't religious if their belief is contingent on data consistency.", "Philosophy of Religion", "A person who believes in God isn't religious if that person's acceptance of that position is contingent on its being consistent with the data."),
    ("It is silly to try to undermine religious belief by arguing it doesn't square with the facts.", "Philosophy of Religion", "This is why it's silly to try to undermine religious belief by arguing that it doesn't square with the facts."),
    ("Religious belief is not subject to views on what inferences the available data warrants.", "Philosophy of Religion", "What distinguishes religious from scientific belief is precisely that the former, unlike the latter, isn't subject to one's views as to what inferences the available data warrants."),
    ("Religious people are right to be unmoved by anti-religious arguments.", "Philosophy of Religion", "And they're right to be unmoved."),
    ("A religious attitude is not marked by subservience to data and logic.", "Philosophy of Religion", "a religious attitude is precisely one that isn't marked by the subservience to data and logic characteristic of the scientific view."),
    ("Attacking religion on scientific or logical grounds is misguided.", "Philosophy of Religion", "those who attack religion on scientific or logical grounds are misguidedly trying to understand religious sentiment in epistemological terms"),
    ("Religious sentiment should be understood in psychoanalytic terms.", "Philosophy of Religion", "when in fact it is to be understood in psychoanalytic terms"),
    ("The philosophy of religion tends to be sterile.", "Philosophy of Religion", "And this, I believe, is part of the reason why the philosophy of religion tends to be so sterile."),
    ("Saying 'God is love' is not the view of somebody who believes in God.", "Philosophy of Religion", "But it isn't the view of somebody who believes in God."),
    ("Attempts to identify God with reason or truth or love are dishonest and incoherent.", "Philosophy of Religion", "Attempts to identify God with reason or truth or love are dishonest and incoherent"),
    ("Religious people have no obligation to defend their views.", "Philosophy of Religion", "religious people have no obligation to defend their views."),
    ("A view that is only as good as the logic and evidence underlying it is a non-religious view.", "Philosophy of Religion", "a view that is only as good as the logic and evidence underlying it is ipso facto a non-religious view."),
    ("Defending a religious view is almost the same as apologizing for it.", "Philosophy of Religion", "Defending a religious view is the same as explaining why one holds it, and explaining why one holds it is almost the same as apologizing for it."),
    ("Many self-described atheists are actually crypto-believers.", "Philosophy of Religion", "many self-described atheists are actually crypto-believers."),
    ("Acceptance of logical or ethical standards can be a distorted expression of belief in God.", "Philosophy of Religion", "Acceptance of such rarefied and depersonalized arbiters of right and wrong is sometimes a distorted and oblique expression of a belief in God."),
    ("There is no relationship between the degree of religiosity and intelligence.", "Philosophy of Religion", "Is there a relationship between the degree to which one is religious and the extent to which one is intelligent? No."),
    ("Religious belief isn't about facts or logic.", "Philosophy of Religion", "religious belief isn't about facts or logic."),
    ("Philosophy has nothing to teach us about religion, with one exception.", "Philosophy of Religion", "There is only one qualification to my previous statement that philosophy has nothing to teach us about religion."),
    ("Plato's Euthyphro argument is cogent.", "Philosophy of Religion", "I consider that argument to be cogent."),
    ("Some acts are inherently good and others are inherently bad.", "Ethics", "Some acts are good and others are bad."),
    ("The goodness of an act is not determined by God's liking it.", "Ethics", "If an act is good, that is because God likes it. In other words, God's liking it is what causes it to be good... Is G correct? No."),
    ("Rape would remain bad even if God liked it.", "Ethics", "What if God liked rape? Would that make it good? No. Rape would be bad even if God liked it, and God would be bad for liking it."),
    ("Acts of kindness would remain good even if God disliked them.", "Ethics", "What if God disliked acts of kindness? Would that make such acts bad? No. They would still be good, and God would be bad for disliking them."),
    ("God has a reason for disliking rape, based on its inherent wrongness.", "Ethics", "Surely God has a good reason for disliking rape. But what could that reason be? The answer is clear: rape is bad; rape is wrong."),
    ("Morality is independent of God's views.", "Ethics", "Conclusion: Morality is independent of God's views."),
    ("God cannot make rape morally good.", "Ethics", "Could God make rape to be morally good? No. Even God cannot make rape be good."),
    ("Even if God speaks to individuals, it is not because of His commands that we believe certain acts are wrong.", "Ethics", "This shows that even if God speaks to certain individuals, it isn't because of what He told them that we believe that rape, theft, and so on, are wrong."),
    ("The Divine Command Theory cannot legitimate existing religious practices or beliefs.", "Ethics", "the Divine Command Theory can do nothing in the way of legitimating existing religious practices or beliefs"),
    ("The existence of bad things suggests either no God or a limited God.", "Theodicy", "This suggests that there is no God or that, if there is a God, He isn't all-powerful, all-good, and all-knowing"),
    ("Theodicies are attempts to show that an all-powerful, all-good, all-knowing God is coherent despite evil.", "Theodicy", "Attempts to show that (d) is coherent are known as theodicies"),
    ("A world with free will is better than a world without it.", "Theodicy", "A world where nothing has free will wouldn't be a very good world."),
    ("A world of robots who do no wrong is not as good as a world of free creatures that do some wrong.", "Theodicy", "A world of robots who do no wrong isn't as good as a world of free creatures that do some wrong"),
    ("God gave humans free will to avoid them being soulless robots.", "Theodicy", "Not wanting us to be soulless robots, God gave us free will"),
    ("Preventing all disasters would prevent human development of character.", "Theodicy", "we, as a species, would never develop any character."),
    ("Life without challenges would be meaningless.", "Theodicy", "if it weren't a challenge, it wouldn't be meaningful."),
    ("A certain amount of strife enriches life, but too much impoverishes it.", "Theodicy", "A certain amount of strife enriches life. But too much impoverishes it."),
    ("There is too much strife for the theodicy to work.", "Theodicy", "There's too much strife for this theodicy to work."),
    ("God cannot make 1 + 1 = 3.", "Omnipotence", "She is unable to make 1 + 1 = 3."),
    ("Something is impossible if the idea of doing it is incoherent.", "Logic", "For something to be impossible is not for it to be very hard to do: it is for the very idea of doing that thing to be an incoherent one."),
    ("Something preexisting itself is logically impossible.", "Logic", "It seems impossible that something should come into existence before it comes into existence."),
    ("Impossibilities are expressed by self-undermining statements.", "Logic", "Impossibilities are expressed by self-undermining statements and, therefore, by non-statements."),
    ("God cannot create a square circle.", "Omnipotence", "I say 'no.'"),
    ("God's inability to create a square circle does not limit Her powers.", "Omnipotence", "this does not show that Her powers are in any way limited."),
    ("A square circle is an impossibility because it involves contradictory definitions.", "Logic", "A square is by definition something that has four straight sides. A circle is by definition something that has no straight sides."),
    ("Impossibility is often mistakenly thought of as a property of things.", "Logic", "We pre-theoretically tend to think of impossibility as a property of things."),
    ("Impossibility is a property of statements, not things.", "Logic", "Impossibility is a property, not of things, but of statements."),
    ("A statement is impossible if it is incoherent.", "Logic", "a statement is impossible if it is incoherent."),
    ("Most incoherent statements contradict themselves implicitly, not explicitly.", "Logic", "We must bear in mind that most incoherent statements contradict themselves implicitly, not explicitly."),
    ("Saying God cannot do the impossible does not imply the existence of impossible objects.", "Omnipotence", "To say that God cannot do the impossible is therefore not to say that there exist certain things that God cannot do."),
    ("There are no impossible objects.", "Logic", "There exist no impossible objects."),
    ("For a statement to be meaningless is for it to have no meaning.", "Logic", "For a statement to be meaningless is for it to have no meaning."),
    ("For a statement to be incoherent is for it to have two or more opposed meanings.", "Logic", "For a statement to be incoherent is for it to have two (or more) opposed meanings."),
    ("Incoherent statements ultimately fail to say anything.", "Logic", "Therefore, my previous statement—that incoherent statements ultimately fail to say anything—has turned out to be true."),
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
    
    for pos_text, topic, quote in religion_positions:
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
    data['database_metadata']['latest_addition'] = f"Philosophy of Religion: +{len(new_positions)} positions with quotes"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 22,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Philosophy of Religion",
            "positions": len(new_positions),
            "topics": ["Philosophy of Religion", "Theodicy", "Euthyphro", "Omnipotence", "Logic", "Ethics"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Philosophy of Religion positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: PR-{max_pr_num+1:03d} to PR-{counter-1:03d}")

if __name__ == "__main__":
    main()
