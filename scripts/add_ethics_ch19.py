#!/usr/bin/env python3
"""
Add Ethics Chapter 19 positions with quotes to the Kuczynski database.
"""

import json
from datetime import datetime

ethics_positions = [
    ("There are two kinds of statements: normative and descriptive.", "Ethics", "There are two kinds of statements: normative and descriptive."),
    ("Descriptive statements do not express value-judgments.", "Ethics", "Descriptive statements don't express value-judgments."),
    ("Normative statements express value-judgments.", "Ethics", "A normative statement is one that does express a value-judgment."),
    ("Ethics is the discipline that attempts to clarify the structure of normative concepts.", "Ethics", "Ethics is the discipline that attempts to clarify the structures of these concepts."),
    ("The term 'good' is ambiguous.", "Ethics", "For each of these terms is ambiguous."),
    ("Instrumental goodness refers to acts that benefit the agent.", "Ethics", "To say that an act is instrumentally good is to say that it has consequences that are desired by, or to the advantage of, the agent."),
    ("Ethics is concerned with intrinsic, not instrumental, goodness.", "Ethics", "Ethics is concerned with intrinsic goodness."),
    ("Ethics asks: 'Which things are intrinsically good?'", "Ethics", "Ethics attempts to answer the question 'which things are intrinsically good?'"),
    ("Happiness, intelligence, benevolence, honesty are examples of intrinsic goods.", "Ethics", "happiness, intelligence, benevolence, honesty… are intrinsically good."),
    ("There are different kinds of freedom: physical, emotional, intellectual.", "Ethics", "there is freedom from external, physical coercion… emotional freedom… intellectual freedom."),
    ("Some things are both instrumentally and intrinsically good.", "Ethics", "Having a sharp intellect is both an intrinsic good and an instrumental good."),
    ("The expression 'intrinsic good' is itself ambiguous.", "Ethics", "the expression 'intrinsic good' is itself ambiguous."),
    ("Some intrinsic goods are praiseworthy; others are not.", "Ethics", "Some things that are intrinsically good are commendable—that is, they deserve praise. And some things that are intrinsically good do not deserve praise."),
    ("Happiness is intrinsically good but not necessarily praiseworthy.", "Ethics", "happiness is non-instrumentally good, while at the same time not being commendable."),
    ("Natural talent is intrinsically good but not praiseworthy.", "Ethics", "Smith's musical talent is intrinsically good… But Smith doesn't deserve any praise for happening to have been blessed with this talent."),
    ("There are two kinds of intrinsic goods: commendable and non-commendable.", "Ethics", "there are two kinds of intrinsic goods—those which are commendable and those which are not."),
    ("There are two kinds of intrinsic badness: condemnable and non-condemnable.", "Ethics", "Just as there are two kinds of intrinsic goodness, so there are two kinds of intrinsic badness."),
    ("Unhappiness is intrinsically bad but not always condemnable.", "Ethics", "It's obviously bad to be unhappy. And the badness in question is clearly of a non-instrumental, and therefore intrinsic, nature."),
    ("Causing unnecessary suffering is both intrinsically bad and condemnable.", "Ethics", "Causing somebody else to suffer, for no good reason, is intrinsically bad and it is condemnable."),
    ("'Intrinsically bad' is not always identical with 'worthy of condemnation.'", "Ethics", "'intrinsically bad' is not, at least not always, identical with 'worthy of condemnation.'"),
    ("A single act can be both intrinsically good and intrinsically bad in different respects.", "Ethics", "A single act or state of affairs can be intrinsically good in one respect and intrinsically bad in some other respect."),
    ("A given act can be both condemnable and commendable.", "Ethics", "A given act can be both condemnable and commendable."),
    ("Moral properties are not privative; they are positive properties.", "Ethics", "Neither property is 'privative'; they are both 'positive' properties."),
    ("Badness is not merely the absence of goodness.", "Ethics", "badness, like goodness, is the presence of something."),
    ("People mistakenly think good and bad cannot coexist because they see them as opposites.", "Ethics", "people tend to think that good and bad cannot co-exist in the same person, or the same act, because they wrongly think that good is the absence of bad."),
    ("People think in binary terms about morality due to cognitive ease.", "Ethics", "People tend, especially where moral and emotional issues are concerned, to think in an unrealistically binary way."),
    ("Moral obligations are not binary; they come in degrees.", "Ethics", "Moral obligations are not 'binary'; they come in degrees."),
    ("Some obligations are stronger than others.", "Ethics", "some obligations are therefore stronger than others."),
    ("There are degrees of wrongness.", "Ethics", "A related point is that there are degrees of wrongness."),
    ("Conflicting obligations can coexist.", "Ethics", "Oftentimes, we have conflicting obligations."),
    ("An overridden obligation still exists.", "Ethics", "obligations that are outweighed by other, more powerful obligations do not on that account cease to exist."),
    ("The right action is the least bad option available.", "Ethics", "what we mean by 'the right course of action' is the least bad course of action that the circumstances permit."),
    ("A wrong action is not necessarily a bad action; it is the least good possible option.", "Ethics", "For a course of action to be wrong is for it to be the least good possible course of action."),
    ("One has an obligation only if one can fulfill it.", "Ethics", "It is a generally accepted principle of ethics that one has an obligation to do something only if one can do it."),
    ("The principle 'ought implies can' must be qualified in cases of conflicting obligations.", "Ethics", "We saw that there are circumstances where one has multiple conflicting obligations… where it isn't strictly correct to say that 'ought' implies 'can.'"),
    ("Legal acts can be immoral.", "Ethics", "There are, or at least can be, acts which are legal, even legally required, which are immoral."),
    ("Legality and morality sometimes overlap.", "Ethics", "At the same time, legality and morality often overlap."),
    ("Knowing a fact does not entitle one to assert it without evidence.", "Ethics", "Given only that some object in fact weighs 200 pounds, I don't necessarily know, or therefore have the right to say, that it has that weight."),
    ("It can be wrong to condemn what is in fact condemnable if one lacks sufficient evidence.", "Ethics", "it can be condemnable to condemn the condemnable."),
    ("Praise depends on intention, not outcome.", "Ethics", "Whether somebody deserves to be commended for an act depends, not on whether it actually was the right act, but on whether it was the agent's intention to perform the right act."),
    ("Two agents with identical intentions deserve the same moral evaluation, regardless of outcome.", "Ethics", "Mary's intentions are exactly like Kathy's… they are equally worthy of praise."),
    ("An agent who intends evil but brings about good still deserves condemnation.", "Ethics", "Betty clearly deserves condemnation of the most severe kind… because, even though she ended up doing good, it was not her intention to do so."),
    ("Failure to commit a crime may indicate lack of resolve or moral reservation.", "Ethics", "failure to carry a plan out successfully oftentimes… suggests that the person's heart wasn't really in it."),
    ("Hitler's intentions were not good.", "Ethics", "it pretty clearly was not Hitler's intention to do good."),
    ("Self-destructive behavior can be immoral.", "Ethics", "One can sell oneself short; one can act self-destructively."),
    ("Self-harm is not morally equivalent to harming others.", "Ethics", "This is not to say that people who hurt themselves are ethically in the same category as people who hurt others."),
    ("Principle-driven acts are not necessarily good.", "Ethics", "Given only that an act is principle-driven, it doesn't follow that it isn't wrong or even evil."),
    ("Punishing self-harm may be ethically worse than the act itself.", "Ethics", "by punishing such a person, we'd be violating their autonomy… which might be ethically worse than what they did."),
    ("Metaethics studies the meaning of ethical statements.", "Metaethics", "Metaethics is the discipline that says what, if anything, ethical statements mean."),
    ("The principle that you cannot derive 'ought' from 'is' may be false.", "Metaethics", "This principle may well be false."),
    ("If certain moral doctrines are correct, 'ought' can be inferred from 'is.'", "Metaethics", "If either of these doctrines… is on target, then an 'ought' can be inferred from 'is.'"),
    ("Moore argued that moral truths are not reducible to descriptive truths.", "Moore", "Ethical truths are not identical with, or otherwise 'reducible to,' factual statements."),
    ("Moore's premise is deeply implausible.", "Moore", "Premise 1 is deeply implausible."),
    ("Moore's argument fails due to a misunderstanding of entailment.", "Moore", "Moore didn't have a very good grasp of the concept of entailment."),
    ("The principle 'ought implies can' is at least approximately correct.", "Metaethics", "Unlike (1) and (2), (3) is at least partly correct—maybe even 100% correct."),
    ("There are counterexamples where obligation persists despite inability.", "Metaethics", "Suppose that you give me $10,000 to move some rocks for you… It still seems that I have an obligation…"),
    ("The origin of a belief is irrelevant to its truth.", "Metaethics", "Whether an idea is correct has to do solely with whether it corresponds to the facts."),
    ("The genetic fallacy occurs when we judge a belief by its origin.", "Metaethics", "In making such a judgment, one commits the genetic fallacy."),
    ("Moral statements can be used for propaganda or evil purposes.", "Ethics", "many moral statements are pure propaganda."),
    ("The misuse of a true moral principle does not negate its truth.", "Ethics", "given that alleged physical laws aren't always actual physical laws, it doesn't follow that there are no physical laws."),
    ("Moral principles are not social inventions.", "Ethics", "Moral principles are not social rules."),
    ("Social enforcement of morality is human-made, but moral truths are not.", "Ethics", "The social institutions that implement moral principles… obviously came into existence at some point in time… But it doesn't follow that moral principles themselves came into existence at that point."),
    ("Disagreement in ethics does not prove ethical non-realism.", "Metaethics", "There appears to be less agreement in ethics than in other disciplines. From this it is concluded that ethical statements merely express 'opinions'… But there are at least four reasons why this is not good reasoning."),
    ("Factual statements can also be disputed without being mere opinion.", "Metaethics", "Consider the statement: If Kennedy hadn't been assassinated… It is exceedingly difficult to know whether KV is an accurate statement or not… But surely it isn't just a 'matter of opinion.'"),
    ("If a statement can be rationally disputed, it likely has an objective basis.", "Metaethics", "any position that can be rationally disputed is likely to have an objective basis."),
    ("Ethical debates often turn on factual questions.", "Ethics", "whether gay marriage is right or wrong depends largely on purely factual issues."),
    ("Many ethical questions have clear, agreed-upon answers.", "Ethics", "Is it morally okay to torture babies for the sheer fun of it? No."),
    ("The illusion of disagreement arises because settled issues are no longer debated.", "Ethics", "The illusion that there is no moral agreement… is that an ethical issue isn't worth discussing anymore if there is universal agreement about it."),
    ("Debates over the death penalty depend on factual questions.", "Ethics", "The question 'how many innocent people are executed for crimes they didn't commit?' is a strictly factual question."),
    ("The abortion debate often turns on factual questions about fetal consciousness.", "Ethics", "Does the fetus have a mind? Can it feel pain?… These are factual questions about the fetus's psychological state."),
    ("Ethical assertions may be disguised factual assertions.", "Metaethics", "ethical assertions are factual assertions, albeit disguised ones."),
    ("Utilitarianism holds that good acts are those that maximize happiness.", "Utilitarianism", "According to one version of it, which is known as 'utilitarianism,' good things are those that bring about happiness."),
    ("Another view holds that good acts promote human flourishing.", "Ethics", "for something to be good is for it to be identical with, or logically required by, a practice on which human flourishing depends."),
    ("If these views are correct, moral questions are factual questions.", "Metaethics", "if the just-described moral view is correct, moral questions are factual questions."),
    ("Normative categories include good, bad, just, unjust, etc.", "Ethics", "Examples of such categories are good, bad, just, unjust, valiant, noble, wicked, depraved, commendable, and condemnable."),
    ("Ethics aims to state the conditions for falling under normative categories.", "Ethics", "ethics attempts to make explicit exactly what conditions an act must satisfy to be praiseworthy."),
    ("Intrinsic goodness is independent of consequences.", "Ethics", "Ethics is interested in identifying those courses of action… that are good even if their consequences are disregarded."),
    ("Helping others without self-interest is intrinsically good.", "Ethics", "Helping a person in need, in cases where doing so is not to one's own practical advantage, is intrinsically good."),
    ("Honesty when inconvenient is intrinsically good.", "Ethics", "Being honest with people, when it would be more convenient to lie, is intrinsically good."),
    ("Intelligence can be both instrumentally and intrinsically good.", "Ethics", "Having intelligence is an instrumental good… But the goodness of being intelligent exceeds any practical advantage."),
    ("A rabbit's happiness is good but not praiseworthy.", "Ethics", "the happiness of a rabbit is a good thing. But… rabbits are not capable of acting in a praiseworthy manner."),
    ("Grieving a loss is not condemnable.", "Ethics", "Somebody who is grieving the loss of a loved one doesn't deserve to be reprimanded."),
    ("Being cold is a privative property (lack of heat).", "Ethics", "For something to be cold is for it to lack heat."),
    ("Being smart is a positive property.", "Ethics", "for something to be hot or smart or rich is not for it to lack anything."),
    ("Condemnability is a positive property.", "Ethics", "The property of being condemnable is not privative; it is a positive property."),
    ("Rocks are neither good nor bad.", "Ethics", "A rock lacks goodness. But rocks aren't bad. They're neither good nor bad."),
    ("Hitler was bad because he had ill-will.", "Ethics", "Hitler was bad. And he was bad because he had something that rocks don't have—he had ill-will."),
    ("Binary moral thinking is emotionally easier.", "Ethics", "It's emotionally easier to see the world as divided into saints and ghouls."),
    ("Conflicting obligations can create moral dilemmas.", "Ethics", "I have a choice: steal the money or let my children die."),
    ("The right action is the lesser of two evils.", "Ethics", "the 'right' thing to do is to steal my friend's money… it is clearly the lesser of two evils."),
    ("Saving fewer lives when more could be saved is wrong.", "Ethics", "If I save the lives of M16–M17, I am obviously doing a good thing… But I'm still doing the wrong thing."),
    ("'Ought implies can' is generally accepted but has exceptions.", "Ethics", "There is much truth in the principle that 'ought' implies 'can.' But… this principle must be taken with a grain of salt."),
    ("Legal acts can be deeply immoral (e.g., slavery).", "Ethics", "it was legal to have slaves, and it was illegal to set another person's slaves free. But it is exceedingly immoral to have slaves."),
    ("One may not have the right to assert a truth without evidence.", "Ethics", "Given only that some statement is correct, I don't necessarily have the right to make it."),
    ("It is wrong to convict without sufficient evidence, even if the person is guilty.", "Ethics", "It is wrong to convict a person that one doesn't know to be guilty, even if that person is guilty."),
    ("Attempted murder is punished less severely because it may indicate lack of intent.", "Ethics", "failure to carry a plan out successfully oftentimes… suggests that the person's heart wasn't really in it."),
    ("One can be immoral toward oneself.", "Ethics", "One can sell oneself short; one can act self-destructively."),
    ("Self-harm is often driven by hyper-principled reasoning.", "Ethics", "People who hurt themselves are often… hyper-principled."),
    ("Punishment is not always warranted for wrongdoing.", "Ethics", "Whether somebody deserves punishment is not a function solely of whether they've done wrong."),
    ("Punishing self-harm may be redundant and harmful.", "Ethics", "self-destructive behavior is its own punishment; so an externally-imposed punishment would be redundant."),
    ("The is-ought gap may be bridgeable.", "Metaethics", "if there is any truth to the thesis that acts are good to the extent that they maximize happiness… then an 'ought' can be inferred from 'is.'"),
    ("Moore's open question argument is flawed.", "Moore", "Moore's argument is no good."),
    ("Entailment can be ampliative (increase knowledge).", "Logic", "Entailment is ampliative."),
    ("The genetic fallacy confuses origin with validity.", "Logic", "The fact that Newton's hypothesis had such a random and ignominious origin is irrelevant to whether it is correct or not."),
    ("Moral truths can exist independently of their social implementation.", "Ethics", "Moral principles are not social rules."),
    ("Ethical disagreement often rests on unresolved factual issues.", "Metaethics", "the seemingly unending nature of this ethical debate has to do… with there being relevant facts that aren't yet in evidence."),
    ("Utilitarianism ties goodness to happiness maximization.", "Utilitarianism", "good things are those that bring about happiness and bad things are those that diminish happiness."),
    ("Human flourishing involves actualizing innate abilities.", "Ethics", "By 'human flourishing' is meant the actualization of human abilities."),
    ("Utilitarianism cannot be completely wrong.", "Utilitarianism", "It's hard to believe that something that made everybody miserable would be good."),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_eth_num = 0
    for pid in existing_ids:
        if pid.startswith('ETH-'):
            try:
                num = int(pid.split('-')[1])
                max_eth_num = max(max_eth_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_eth_num + 1
    
    for pos_text, topic, quote in ethics_positions:
        pos_id = f"ETH-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"ETH-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Ethics Ch19 - J.-M. Kuczynski",
            "work_id": "WORK-ETHICS-CH19",
            "domain": "ethics"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Ethics Ch19: +{len(new_positions)} positions"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 25,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Ethics Ch19",
            "positions": len(new_positions),
            "topics": ["Ethics", "Metaethics", "Utilitarianism", "Moore", "Logic"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Ethics Ch19 positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: ETH-{max_eth_num+1:03d} to ETH-{counter-1:03d}")

if __name__ == "__main__":
    main()
