#!/usr/bin/env python3
"""
Add Analytic Philosophy Chapter 20 positions with quotes to the Kuczynski database.
Topics: Emotivism, Value-Nihilism, Aesthetics, Emotions as Beliefs
"""

import json
from datetime import datetime

ch20_positions = [
    ("Ethical statements, when sincere, inherently express feelings or emotions.", "Emotivism", "According to some, it is inherent in the nature of ethical pronouncements that, when made sincerely, they express feelings or emotions of some kind."),
    ("A purely factual statement does not reveal the speaker's feelings.", "Emotivism", "Given only that you've sincerely said 'that rock weighs over 100 pounds,' nothing can be concluded about how you feel about the rock's weight."),
    ("A sincere moral judgment must embody some feeling about its subject.", "Emotivism", "if you say 'Larry is a bad man,' your statement, if sincere, must embody feelings of some kind concerning Larry's deeds or character."),
    ("To make a moral statement without feeling is insincere.", "Emotivism", "If you feel nothing either way, you're guilty of insincerity in uttering that sentence…"),
    ("Emotivism suggests moral 'judgments' are merely expressions of sentiment.", "Emotivism", "these points suggest that moral 'judgments' are nothing more than expressions of sentiment."),
    ("Saying 'Larry is a bad man' is just venting negative feelings.", "Emotivism", "If you say 'Larry is a bad man,' you're just venting your negative feelings about Larry…"),
    ("Moral statements are no more true or false than facial expressions.", "Emotivism", "you're no more saying something true or false than you would be if you scowled at Larry."),
    ("'Stealing is wrong' is equivalent to saying 'boo stealing!'", "Emotivism", "'Stealing is wrong' is just a way of saying 'boo stealing!'…"),
    ("If emotivism is true, there are no moral truths or falsehoods.", "Emotivism", "Consequently, there are no moral truths and no moral falsehoods."),
    ("It is false that 'x is good' means 'hurray x!'", "Emotivism", "It's simply false that saying 'x is good' is tantamount to saying 'hurray x!'"),
    ("One can sincerely make a moral judgment without personal emotion.", "Emotivism", "a competent speaker of English can sincerely say 'Cotton Mather was a good man' without personally having any emotion…"),
    ("People can coolly make moral judgments.", "Emotivism", "It's clear that people can coolly make moral judgments."),
    ("Emotion-driven judgment is not an unbiased ethical judgment.", "Emotivism", "an emotion-driven judgment is, to that extent, not an ethical judgment—or, in any case, not an unbiased one."),
    ("One can make positive moral judgments about displeasing things.", "Emotivism", "One often makes positive moral judgments about people and things that bring them displeasure."),
    ("One can judge an act as good while personally disliking it.", "Emotivism", "There are people who I dislike whose noble acts make me want to wretch. But… I do judge that those acts are good."),
    ("Hume provided a compelling answer on reconciling moral judgment with emotion.", "Hume", "David Hume… provided a compelling answer to this question…"),
    ("Artistic goodness is often linked to giving pleasure.", "Aesthetics", "In general, people regard artistic works that bring them pleasure as 'good'…"),
    ("'x is good' in art might seem to mean 'x gives me pleasure.'", "Aesthetics", "…when said of a work of art, 'x is good' means 'x gives me pleasure'…"),
    ("The pleasure analysis of artistic goodness cannot be right.", "Aesthetics", "But this analysis cannot quite be right."),
    ("One can judge a pleasure-less work as good.", "Aesthetics", "People can, without self-contradiction, judge that works that don't bring them pleasure are 'good'…"),
    ("Irrelevant personal factors can inhibit pleasure from a good work.", "Aesthetics", "This happens when people know that they would like a given work were it not for the inhibiting influence of some plainly irrelevant factor."),
    ("One can know a work is good even if it brings personal torture.", "Aesthetics", "So you know that it's good, even though… it doesn't bring you pleasure."),
    ("'Good' in art means it brings pleasure setting aside irrelevancies.", "Aesthetics", "when people describe a work of art as 'good,' they mean that, setting aside irrelevancies… it brings people pleasure."),
    ("The same principle applies mutatis mutandis in the moral sphere.", "Ethics", "The same thing mutatis mutandis holds in the moral sphere."),
    ("People can regard pleasure-less acts as moral.", "Ethics", "people sometimes regard things that bring them no pleasure, or even displeasure, as 'moral'…"),
    ("People can regard pleasure-bringing acts as immoral.", "Ethics", "they sometimes regard things that bring them acute pleasure as 'immoral.'"),
    ("A criminal may commend his own punishment.", "Ethics", "Many a person has committed heinous crimes and then commended the government for putting him in jail."),
    ("'x is good' means 'x makes people happy barring idiosyncratic factors.'", "Ethics", "'x is good' means 'x makes people happy to the extent so far as individual-specific, non-transferable facts about them aren't a factor.'"),
    ("Hume's argument shows emotivism must be changed to be credible.", "Emotivism", "Hume's powerful argument shows that, if it is to be credible, emotivism must be changed…"),
    ("One can judge something good even if it brings misery.", "Ethics", "a person can judge that something is good even if that thing brings him misery…"),
    ("Therefore, 'x is good' cannot be expressing happiness about x.", "Emotivism", "…saying 'x is good' cannot possibly be the same thing as expressing one's happiness about x."),
    ("'x is good' may express belief that x is happiness-conducive.", "Emotivism", "But 'x is good' is plausibly seen as expressing the speaker's belief that x is happiness-conducive…"),
    ("Thus modified, emotivism is blatantly false.", "Emotivism", "But, thus modified, emotivism is blatantly false."),
    ("If 'x is good' expresses a belief, it is true or false.", "Emotivism", "If it expresses any belief, 'x is good' is either true or false."),
    ("The essence of emotivism is that moral statements express feelings, not judgments.", "Emotivism", "The essence of emotivism is that 'x is good' expresses a feeling, as opposed to a judgment…"),
    ("Modified emotivism collapses into its opposite.", "Emotivism", "So emotivism collapses into its opposite if it's modified along the lines suggested by Hume."),
    ("Modified emotivism coincides with utilitarianism.", "Emotivism", "thus modified, emotivism coincides with utilitarianism."),
    ("Hume's analysis (HA) is viciously circular.", "Hume", "What is more, HA is viciously circular."),
    ("One must distinguish between enjoying something and being caused pleasure by it.", "Aesthetics", "It's crucial to distinguish between enjoying something, on the one hand, and being caused by it to experience pleasure, on the other."),
    ("Being caused joy by X is not the same as enjoying X.", "Aesthetics", "Here the G-minor ballad is causing me joy; but I'm not enjoying it."),
    ("When this distinction is recognized, emotivism collapses.", "Emotivism", "When this distinction is given its due, emotivism collapses…"),
    ("Value-nihilism also collapses with this distinction.", "Value-Nihilism", "…and so does every form of value-nihilism."),
    ("Value-nihilism: 'x is good' means nothing or means x is liked.", "Value-Nihilism", "By 'value-nihilism' I mean any doctrine to the effect that 'x is good' either means nothing or means that x is liked or otherwise looked upon favorably…"),
    ("Not all reasons for feeling good are aesthetic.", "Aesthetics", "Not all of those reasons are of an aesthetic nature."),
    ("A genuine aesthetic reaction is driven by a thing's artistic merits.", "Aesthetics", "…what makes Jones feel good is X's having certain artistic merits."),
    ("If there are aesthetic reactions, there are aesthetic facts.", "Aesthetics", "So to the extent that there are aesthetic reactions, there are aesthetic facts…"),
    ("If there are aesthetic facts, we can be wrong about them.", "Aesthetics", "If there are aesthetic facts, we can be wrong about them, just as we can be wrong about anything else."),
    ("If there are aesthetic facts, value-nihilism is false regarding aesthetics.", "Value-Nihilism", "So if there are aesthetic facts, value-nihilism is false, at least as far as aesthetic properties are concerned."),
    ("The saying 'there's no disputing taste' is invoked against aesthetic facts.", "Aesthetics", "Everyone knows the old saying: 'there's no disputing taste.'"),
    ("Aesthetic facts don't imply all works are comparable.", "Aesthetics", "…it doesn't follow that, given any two works of musical works… they are capable of being meaningfully compared."),
    ("Works can be good in non-comparable ways.", "Aesthetics", "they are good in non-comparable ways."),
    ("Their goodness may be 'incommensurable.'", "Aesthetics", "The goodness of any one of them is 'incommensurable'… with the goodness of either of the others."),
    ("Not every musical work is as good as every other.", "Aesthetics", "But that doesn't mean that every musical work is as good as every other musical work."),
    ("It's obvious some composers are better than others.", "Aesthetics", "In any case, it's patently obvious that some composers are better than others."),
    ("No musician can coherently believe all works are of equal merit.", "Aesthetics", "And no such musician can coherently believe that no musical work is better than any other."),
    ("Moral nihilism fails for similar reasons as aesthetic nihilism.", "Value-Nihilism", "Moral nihilism fails for much the same reasons that aesthetic nihilism fails."),
    ("A moral reaction requires S's moral properties cause the joy.", "Ethics", "It's only if S's having such and such moral properties is what brings me joy that my liking S is a moral reaction to it."),
    ("There are moral reactions only if there are moral facts.", "Ethics", "In general, there are moral reactions only to the extent that there are moral facts."),
    ("If there are moral facts, emotivism collapses.", "Emotivism", "If there are moral facts, our feelings may or may not do them justice; and emotivism completely collapses."),
    ("Sense-perceptions represent the world as being a certain way.", "Epistemology", "Our sense-perceptions represent the world as being a certain way."),
    ("Sense-perceptions have truth-conditions.", "Epistemology", "…they have 'truth-conditions': they're accurate iff the world satisfies certain conditions."),
    ("The common view: emotions are neither true nor false.", "Emotions", "Emotions can be healthy or unhealthy, but they cannot be true or false."),
    ("Emotions typically involve presuppositions about the world.", "Emotions", "Of course, emotions typically involve presuppositions about how the world is."),
    ("You cannot be angry that Tim stole your bike unless you believe he did.", "Emotions", "You cannot be angry that Tim stole your bicycle unless you believe that Tim stole your bicycle."),
    ("Emotions presuppose beliefs but aren't themselves beliefs.", "Emotions", "Emotions presuppose beliefs; but emotions aren't themselves beliefs."),
    ("This view is attributed to David Hume.", "Hume", "The position just described was advocated by David Hume…"),
    ("Hume's view is totally false.", "Emotions", "Hume's view, we will now see, is totally false."),
    ("Emotions are true or false.", "Emotions", "Emotions are true or false."),
    ("Emotions are beliefs.", "Emotions", "The reason is that, counterintuitive though it may seem, emotions are beliefs."),
    ("We'd see taking a pill to wipe out emotions as self-lobotomizing.", "Emotions", "But that is how we'd regard somebody who took a pill that wiped away all his unpleasant emotions."),
    ("People want circumstances to change so emotions become inappropriate.", "Emotions", "What they want is to change their circumstances in such a way that their unpleasant emotions no longer have a basis in them."),
    ("People don't want to 'zap' emotions; they want the world to change.", "Emotions", "People don't want to 'zap' their anger or hate or pessimism. They want the world to change… that those emotions cease to be appropriate."),
    ("Attitude toward emotions is like attitude toward senses: we want accurate representation.", "Emotions", "In this respect, the attitude that people have towards their emotions is similar to the attitude they have towards their senses."),
    ("People want to feel joy because circumstances warrant it.", "Emotions", "And people want to feel joy. But they want to feel it because their circumstances warrant it…"),
    ("Like perceptions, emotions have an object.", "Emotions", "Like a sense-perception or thought, an emotion must have an object."),
    ("You can't just be angry; you're angry at or about something.", "Emotions", "You can't just be angry. You're angry at your boss for giving someone else the promotion."),
    ("Causing an emotion is not the same as being its object.", "Emotions", "Given only that x is what caused so and so to have emotion y, it doesn't follow that x is what… so and so is emoting about."),
    ("Having a negative emotion about X isn't being caused by X to have it.", "Emotions", "This confirms that having a negative emotion about X isn't the same thing as being caused by X to have a negative emotion."),
    ("Happiness is the recognition that one can now gratify a desire.", "Emotions", "Ben's being happy that he can play soccer is his recognition that… he can now gratify an otherwise ungratifiable desire."),
    ("The analysis extends to all emotions.", "Emotions", "This analysis is easily extended to apply to all emotions."),
    ("Fear involves believing a desire is jeopardized.", "Emotions", "So, to fear her coming is for you to believe that her coming would frustrate some desire of yours."),
    ("Emotions are beliefs about the prospects of gratifying desires.", "Emotions", "Emotions, then, are beliefs about the prospects of gratifying desires that one has."),
    ("Positive emotion: belief prospects are good.", "Emotions", "If the belief is that the prospects are good, the emotion is a positive one…"),
    ("Negative emotion: belief prospects are bad.", "Emotions", "If the belief is that those prospects are bad, it's a negative one…"),
    ("Geach put forth a clever argument against emotivism.", "Emotivism", "Peter Geach put forth the following, very clever argument against emotivism…"),
    ("Geach's argument substitutes 'boo stealing!' for 'stealing is wrong.'", "Emotivism", "Suppose that saying 'stealing is wrong' is… no different from saying 'boo stealing!'…"),
    ("Replacing with a synonym shouldn't turn meaning into nonsense.", "Logic", "Replacing an expression with a synonymous expression doesn't turn meaning into nonsense…"),
    ("(1) is meaningful; (2) is nonsense.", "Logic", "But whereas (1) is obviously meaningful… (2) is complete nonsense."),
    ("Therefore, the expressions are not synonymous; emotivism is wrong.", "Emotivism", "Thus, the underlined expressions are not synonymous, and the emotivist is wrong to say otherwise."),
    ("If emotions are beliefs, Geach's argument fails.", "Emotivism", "Which makes it obvious that Geach's argument fails if emotions are beliefs."),
    ("Geach's argument makes a strong, unargued, probably false assumption.", "Emotivism", "Which, in its turn, shows that it makes a strong, unargued, and probably false assumption."),
    ("Therefore, Geach's argument is spurious.", "Emotivism", "Which, finally, shows that it's spurious."),
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
    
    for pos_text, topic, quote in ch20_positions:
        pos_id = f"AP-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"AP-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "quote": quote,
            "source": "Analytic Philosophy Ch20 - J.-M. Kuczynski",
            "work_id": "WORK-ANALYTIC-CH20",
            "domain": "analytic_philosophy"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Analytic Philosophy Ch20: +{len(new_positions)} positions"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 26,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Analytic Philosophy Ch20",
            "positions": len(new_positions),
            "topics": ["Emotivism", "Value-Nihilism", "Aesthetics", "Emotions", "Hume"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Analytic Philosophy Ch20 positions with quotes.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: AP-{max_ap_num+1:03d} to AP-{counter-1:03d}")

if __name__ == "__main__":
    main()
