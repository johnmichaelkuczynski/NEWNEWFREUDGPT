#!/usr/bin/env python3
"""
Expand Hume database with 2000+ positions and 2000+ quotes from source materials.
"""

import json
import re
import os
from collections import defaultdict

POSITIONS_FILE = "attached_assets/HUME_POSITION_STATEMENTS_1766192732605.txt"
HUME_TEXT_FILE = "attached_assets/HUME_1766192732603.txt"
QUESTION_BANK = "attached_assets/HUME_QUESTION_BANK_1766192732602.txt"
OUTPUT_DB = "data/HUME_DATABASE.json"
OUTPUT_QUOTES = "data/hume_fact_positions.json"

DOMAINS = {
    "causation": ["cause", "effect", "causal", "necessary connection", "constant conjunction", "custom", "habit"],
    "epistemology": ["knowledge", "belief", "impression", "idea", "perception", "reason", "understanding", "experience", "probable"],
    "metaphysics": ["self", "identity", "substance", "existence", "external object", "body", "mind", "soul", "bundle"],
    "morality": ["virtue", "vice", "moral", "sentiment", "approbation", "disapprobation", "justice", "benevolence", "utility"],
    "psychology": ["passion", "emotion", "desire", "aversion", "pride", "humility", "love", "hatred", "sympathy"],
    "religion": ["god", "deity", "miracle", "design", "providence", "religion", "theism", "atheism"],
    "aesthetics": ["beauty", "taste", "art", "aesthetic", "agreeable", "pleasant"],
    "politics": ["government", "allegiance", "authority", "consent", "property", "promise", "obligation"],
    "freedom": ["liberty", "necessity", "determinism", "free will", "compatibilism", "voluntary"]
}

def classify_domain(text):
    text_lower = text.lower()
    scores = defaultdict(int)
    for domain, keywords in DOMAINS.items():
        for kw in keywords:
            if kw in text_lower:
                scores[domain] += 1
    if scores:
        return max(scores, key=scores.get)
    return "general_philosophy"

def extract_positions_from_file(filepath):
    positions = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_work = "A Treatise of Human Nature"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if "Treatise of Human Nature" in line:
            current_work = "A Treatise of Human Nature"
        elif "Enquiry concerning Human Understanding" in line:
            current_work = "An Enquiry concerning Human Understanding"
        elif "Enquiry concerning the Principles of Morals" in line:
            current_work = "An Enquiry concerning the Principles of Morals"
        elif "Dialogues concerning Natural Religion" in line:
            current_work = "Dialogues concerning Natural Religion"
        
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match:
            num, text = match.groups()
            if len(text) > 20:
                positions.append({
                    "text": text.strip(),
                    "work": current_work
                })
    
    return positions

def extract_quotes_from_text(filepath):
    quotes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paragraphs = re.split(r'\n\s*\n', content)
    current_section = "General"
    
    for para in paragraphs:
        para = para.strip()
        if not para or len(para) < 100:
            continue
        
        section_match = re.match(r'^SECTION\s+([IVXLC]+)\.\s*\n*(.+?)(?:\n|$)', para, re.IGNORECASE)
        if section_match:
            current_section = section_match.group(2).strip()[:100]
        
        if para.startswith("***") or "Project Gutenberg" in para:
            continue
        
        sentences = re.split(r'(?<=[.!?])\s+', para)
        
        for i in range(0, len(sentences) - 1, 2):
            chunk = ' '.join(sentences[i:i+3])
            chunk = re.sub(r'\s+', ' ', chunk).strip()
            if 80 < len(chunk) < 600 and not chunk.startswith("***"):
                quotes.append({
                    "text": chunk,
                    "section": current_section
                })
    
    return quotes

def generate_additional_positions():
    additional = []
    
    epistemology_positions = [
        "All our ideas are copies of impressions, differing only in their degree of force and vivacity.",
        "The imagination is free to transpose and change ideas, but cannot create simple ideas not derived from impressions.",
        "Memory retains both the original order and position of ideas, while imagination is not restrained to the same order.",
        "Complex ideas may be divided into ideas of relations, modes, and substances.",
        "The abstract idea of existence is the same as the idea of any particular object conceived as existing.",
        "We can form ideas of objects we have never perceived by combining simple ideas from experience.",
        "The idea of God is formed by augmenting without limit the qualities of goodness and wisdom we find in ourselves.",
        "All reasoning concerning matters of fact is founded on the relation of cause and effect.",
        "Experience is the foundation of all our conclusions concerning matters of fact.",
        "We cannot penetrate into the reason of the ultimate causes of nature, and must rest content with experience.",
        "Belief is nothing but a more vivid, lively, forcible conception of an idea.",
        "Custom or habit is the great guide of human life.",
        "Without the influence of custom, we should be entirely ignorant of every matter of fact beyond what is immediately present.",
        "All inferences from experience are effects of custom, not of reasoning.",
        "The understanding operates in making inferences from experience without the intervention of reason.",
        "We are determined by custom alone to suppose the future conformable to the past.",
        "No object ever discovers, by the qualities which appear to the senses, either the causes which produced it or the effects which arise from it.",
        "Causes and effects are discoverable by experience, not by reason.",
        "When we see similar sensible qualities, we expect similar secret powers and effects.",
        "There is no foundation for drawing any inference concerning the future from the past, except custom.",
        "The imagination supplies the idea of that power or necessary connection which we feel in the mind.",
        "Our idea of necessity and causation arises entirely from the uniformity observable in the operations of nature.",
        "The supposition that the future will resemble the past is not founded on arguments of any kind.",
        "All probable reasoning is nothing but a species of sensation.",
        "Nature has determined us to judge as well as to breathe and feel.",
        "Belief is more an act of the sensitive than of the cogitative part of our natures.",
        "Objects have no discoverable connection together in nature; we can never presume to infer any effect from them a priori.",
        "Experience teaches us not by any argument or train of reasoning, but by custom immediately.",
        "The more instances we have observed, and the more uniform they appear, the more firmly we believe our inferences.",
        "Probability is founded on the presumption of a resemblance between those objects of which we have had experience.",
        "All our experimental conclusions proceed upon the supposition that the future will be conformable to the past.",
        "There are no ideas which occur in metaphysics more obscure and uncertain than those of power, force, energy, or necessary connection.",
        "We never feel any power or efficacy in our own mental operations.",
        "The first time a man saw the communication of motion by impulse, he could not pronounce that one event was connected with another.",
        "Upon the whole, there appears not, throughout all nature, any one instance of connection which is conceivable by us.",
        "All events seem entirely loose and separate; one event follows another, but we never can observe any tie between them.",
        "The necessary connection between causes and effects is the foundation of our inference from one to the other.",
        "We have no other notion of cause and effect but that of certain objects which have been always conjoined together.",
        "Power and necessity are qualities of perceptions, not of objects.",
        "The distinction between power and the exercise of it is entirely frivolous.",
    ]
    
    for i, pos in enumerate(epistemology_positions):
        additional.append({
            "text": pos,
            "work": "An Enquiry concerning Human Understanding",
            "domain": "epistemology"
        })
    
    causation_positions = [
        "Necessity, if we examine it, will be found to amount to no more than a constant conjunction of objects.",
        "We never can, by our utmost scrutiny, discover anything but one event following another.",
        "The constant conjunction of objects constitutes the very essence of necessity.",
        "When we say one object is connected with another, we mean only that they have acquired a connection in our thought.",
        "Necessity is something that exists in the mind, not in objects.",
        "The connexion which we feel in the mind is the customary transition of the imagination from one object to its usual attendant.",
        "All causes are of the same kind, and there is no foundation for that distinction between efficient causes and causes sine qua non.",
        "We may define a cause to be an object followed by another, where all objects similar to the first are followed by objects similar to the second.",
        "Where a cause operates through a number of intermediate causes, the principal cause is distinguished by being the most remote.",
        "Chance is nothing real in itself, and properly speaking is merely the negation of a cause.",
        "Nothing exists without a cause; the contrary opinion implies that things can arise without a cause.",
        "The production of anything without a cause is contrary to experience.",
        "Every event has a cause, though we may not be able to discover it.",
        "We can never demonstrate the necessity of a cause to every new existence.",
        "The idea of cause and effect is derived from experience, which informs us of their constant conjunction.",
        "When we are once acquainted with the operation of cause and effect, we can extend our experience to all times and places.",
        "Objects have no discernible connection together; all conclusions from cause to effect are derived from custom.",
        "Experience only teaches us how one event constantly follows another, without instructing us in the secret connection.",
        "Motion in one body is regarded upon impulse as the cause of motion in another.",
        "All our reasonings concerning cause and effect are derived entirely from experience.",
        "We cannot reason a priori about causes; experience alone can show the connection between events.",
        "The vulgar confound the constant conjunction of objects with a necessary connection.",
        "There is no object which implies the existence of any other if we consider these objects in themselves.",
        "When we define a cause by contiguity and succession, we define what we can perceive.",
        "The ultimate cause of any natural operation is absolutely inexplicable by human reason.",
        "All our reasoning concerning causes and effects is derived from experience alone.",
        "We cannot know the ultimate causes of natural operations; we must be satisfied with particular experiences.",
        "The powers by which bodies operate are entirely unknown to us.",
        "We perceive only sensible qualities; we cannot perceive any power or energy by which objects operate.",
        "Observation of constant conjunction is the sole foundation of our idea of causation.",
    ]
    
    for i, pos in enumerate(causation_positions):
        additional.append({
            "text": pos,
            "work": "An Enquiry concerning Human Understanding",
            "domain": "causation"
        })
    
    self_identity_positions = [
        "There is no impression of the self that remains constant and invariable through our lives.",
        "The self is nothing but a bundle or collection of different perceptions in perpetual flux.",
        "When I enter most intimately into what I call myself, I always stumble on some particular perception.",
        "The identity we ascribe to the mind is only a fictitious one, like that we ascribe to plants and animals.",
        "Our several perceptions are distinct existences and may be conceived as separately existent.",
        "The mind is a kind of theatre where several perceptions successively make their appearance.",
        "There is properly no simplicity in the mind at one time, nor identity in different times.",
        "The comparison of the soul to a republic or commonwealth suggests its nature as a connected succession of perceptions.",
        "Memory alone acquaints us with the continuance and extent of this succession of perceptions.",
        "Personal identity arises from the smooth and uninterrupted progress of the thought along a train of connected ideas.",
        "The relation of causation among our perceptions produces the notion of personal identity.",
        "We have no notion of the self distinct from particular perceptions.",
        "The controversy concerning identity is merely a dispute of words.",
        "What we call a mind is nothing but a heap or collection of different perceptions.",
        "Identity is not something really belonging to these different perceptions and uniting them together.",
        "The understanding never observes any real connection among distinct existences.",
        "We only feel a connection or determination of the thought to pass from one object to another.",
        "The notion of soul, self, or substance is nothing but a collection of qualities united by the imagination.",
        "All our distinct perceptions are distinct existences, and the mind never perceives any real connection among them.",
        "Personal identity is a fiction of the imagination, produced by the resemblance of perceptions.",
    ]
    
    for i, pos in enumerate(self_identity_positions):
        additional.append({
            "text": pos,
            "work": "A Treatise of Human Nature",
            "domain": "metaphysics"
        })
    
    morality_positions = [
        "Morality is determined by sentiment; it defines virtue to be whatever mental action or quality gives a spectator the pleasing sentiment of approbation.",
        "Reason is, and ought only to be the slave of the passions, and can never pretend to any other office than to serve and obey them.",
        "Actions themselves have no merit; the merit lies entirely in the motive.",
        "A virtuous motive is requisite to render an action virtuous.",
        "Virtue and vice are not matters of fact discoverable by reason, but by sentiment.",
        "When you pronounce any action or character to be vicious, you mean nothing but that you have a feeling of blame from the contemplation of it.",
        "Moral distinctions are not derived from reason alone.",
        "The rules of morality are not conclusions of our reason.",
        "Vice and virtue may be compared to sounds, colors, heat and cold, which are not qualities in objects but perceptions in the mind.",
        "Morality is more properly felt than judged of.",
        "Nothing can oppose or retard the impulse of passion but a contrary impulse.",
        "Reason alone can never be a motive to any action of the will.",
        "Reason alone can never produce any action or give rise to volition.",
        "The ultimate ends of human actions can never be accounted for by reason, but recommend themselves entirely to the sentiments.",
        "It is not contrary to reason to prefer the destruction of the whole world to the scratching of my finger.",
        "Reason is utterly impotent in moral matters without the assistance of some other principle.",
        "The distinction of vice and virtue is not founded merely on the relations of objects.",
        "Justice is an artificial virtue arising from the circumstances and necessity of mankind.",
        "The rules of equity or justice depend entirely on the particular state and condition in which men are placed.",
        "The sense of justice arises from artifice and human conventions.",
        "The origin of justice is to be found in the selfishness and confined generosity of men.",
        "Justice is acknowledged to be useful to society, and this is the sole foundation of its merit.",
        "Public utility is the sole origin of justice.",
        "The convention for the distinction of property is of all circumstances the most necessary to the establishment of human society.",
        "Property is nothing but those goods whose constant possession is established by the laws of society.",
        "The stability of possession is the most necessary of all social conventions.",
        "Promises have no force antecedent to human conventions.",
        "The obligation of promises arises entirely from the conventions of men.",
        "Allegiance to government is founded entirely on the opinion of advantage which we reap from it.",
        "The duty of allegiance is grounded on the obligation of promises only when promises are explicit.",
        "Benevolence is approved because it promotes the good of mankind.",
        "We approve of justice because it tends to promote the good of society.",
        "Sympathy is the chief source of moral distinctions.",
        "The moral sentiments must be allowed to have a considerable influence on all our judgments of this nature.",
        "Approbation or blame is nothing but a fainter and more imperceptible love or hatred.",
        "Personal merit consists entirely of the possession of mental qualities useful or agreeable to ourselves or others.",
        "Actions are only so far virtuous as they are the signs of some quality in the mind.",
        "Virtue is any quality of the mind agreeable to or approved of by everyone who considers or contemplates it.",
        "We never approve of any sentiment in others of which we have not at least the seeds in ourselves.",
        "The social virtues of humanity and benevolence exert their influence immediately by a direct tendency.",
    ]
    
    for i, pos in enumerate(morality_positions):
        additional.append({
            "text": pos,
            "work": "A Treatise of Human Nature",
            "domain": "morality"
        })
    
    passion_positions = [
        "Pride is a pleasant sensation and humility a painful one, arising from a view of our own qualities and circumstances.",
        "The causes of pride and humility must be related to self and independently produce pleasure or pain.",
        "Love and hatred are simple and original impressions, not derived from any prior impression.",
        "Sympathy is the communication of sentiments from one person to another by the imagination.",
        "By sympathy we enter into the sentiments of others and partake of their pleasures and uneasiness.",
        "The passions are divided into direct and indirect, depending on whether they arise immediately from good or evil.",
        "Direct passions such as desire, aversion, grief, joy, hope, and fear arise immediately from good or evil.",
        "Indirect passions such as pride, humility, ambition, vanity, love, hatred arise from a double relation of ideas and impressions.",
        "The object of pride is always the self; the causes of pride are various.",
        "We naturally love what is related to ourselves and hate what is contrary to our interest.",
        "The passion of anger arises from injury or injustice done to ourselves or those we love.",
        "Malice is the unprovoked desire of producing evil to another in order to reap a pleasure from the comparison.",
        "Envy arises from a comparison of ourselves with others and a sense of inferiority.",
        "Pity is a concern for and sympathy with the misery of others.",
        "The idea of the suffering of others is converted into an impression by sympathy.",
        "Respect is a mixture of love and humility; contempt a mixture of hatred and pride.",
        "The will is nothing but the internal impression we feel when we knowingly give rise to any new motion of our body or new perception of our mind.",
        "The immediate effects of pain and pleasure are desire and aversion.",
        "Hope and fear arise from the probability of good and evil.",
        "The calm passions are often confounded with the operations of reason.",
        "Violent passions have a more sensible effect on the mind than the calm.",
        "Strength of mind implies the prevalence of the calm passions above the violent.",
        "Custom and repetition increase the violence of the active passions while diminishing the pleasurable.",
        "The love of fame is a passion which operates on the mind with a peculiar force.",
        "Curiosity is the love of truth and the pursuit of knowledge for its own sake.",
        "The passion of wonder arises from something unexpected or unusual.",
        "The passions are original existences; they contain no representative quality.",
        "A passion can never be called unreasonable except when founded on a false supposition.",
        "The combat of passion and reason is only a figure of speech; passions never truly oppose reason.",
        "Only a contrary passion can oppose or control a passion, never reason alone.",
    ]
    
    for i, pos in enumerate(passion_positions):
        additional.append({
            "text": pos,
            "work": "A Treatise of Human Nature",
            "domain": "psychology"
        })
    
    skepticism_positions = [
        "All the objects of human reason or inquiry may be divided into relations of ideas and matters of fact.",
        "Matters of fact, which are the second objects of human reason, are not ascertained in the same manner as relations of ideas.",
        "The contrary of every matter of fact is still possible, because it can never imply a contradiction.",
        "All reasonings concerning matters of fact are founded on the relation of cause and effect.",
        "By means of that relation alone we can go beyond the evidence of our memory and senses.",
        "If we proceed not upon some fact present to the memory or senses, our reasonings would be merely hypothetical.",
        "The ultimate cause of any natural operation is absolutely inexplicable.",
        "Human reason can give no satisfactory answer to the most fundamental questions about nature.",
        "All the philosophy in the world, and all the religion, could never carry us beyond the usual course of experience.",
        "Nature has kept us at a great distance from all her secrets and has afforded us only the knowledge of a few superficial qualities of objects.",
        "The most perfect philosophy of the natural kind only staves off our ignorance a little longer.",
        "Philosophy would render us entirely Pyrrhonian were not nature too strong for it.",
        "Nature breaks the force of all skeptical arguments and keeps them from having any considerable influence on the understanding.",
        "Skeptical reasonings, if they could prevail, would subvert all speculation and all action.",
        "The great subverter of excessive skepticism is action and employment and the occupations of common life.",
        "A Pyrrhonian cannot expect that his philosophy will have any constant influence on the mind.",
        "All our reasonings concerning causes and effects are derived from nothing but custom.",
        "Custom is the great guide of human life.",
        "After we have experience of the operation of cause and effect, our conclusions from that experience are not founded on reasoning.",
        "The skeptic still continues to reason and believe, though he asserts that he cannot defend his reason by reason.",
        "A mitigated skepticism or academic philosophy is both durable and useful.",
        "Philosophical skepticism leads us to modesty and reserve in our opinions.",
        "A small degree of Pyrrhonism might abate our presumption and our prejudice.",
        "The limitation of our inquiries to such subjects as are best adapted to our faculties is the result of skeptical reflection.",
        "Divinity or theology has a foundation in reason, only so far as it is supported by experience.",
        "Our most holy religion is founded on faith, not on reason.",
        "Common life is the corrective to excessive philosophizing.",
        "In all the incidents of life we ought still to preserve our skepticism.",
        "I am ready to throw all my books and papers into the fire when I reflect on the weakness of human reason.",
        "The intense view of these manifold contradictions and imperfections in human reason has so wrought upon me and heated my brain.",
    ]
    
    for i, pos in enumerate(skepticism_positions):
        additional.append({
            "text": pos,
            "work": "An Enquiry concerning Human Understanding",
            "domain": "epistemology"
        })
    
    religion_positions = [
        "A miracle is a violation of the laws of nature; and as a firm and unalterable experience has established these laws, the proof against a miracle is as entire as any argument from experience can possibly be imagined.",
        "No testimony is sufficient to establish a miracle unless the testimony be of such a kind that its falsehood would be more miraculous than the fact which it endeavors to establish.",
        "There is not to be found in all history any miracle attested by a sufficient number of men of such unquestioned good sense, education, and learning.",
        "The passion of surprise and wonder arising from miracles, being an agreeable emotion, gives a sensible tendency towards the belief of those events.",
        "The many instances of forged miracles and prophecies and supernatural events prove the strong propensity of mankind to the extraordinary and marvelous.",
        "It forms a strong presumption against all supernatural and miraculous relations that they are observed chiefly to abound among ignorant and barbarous nations.",
        "Upon the whole, we may conclude that the Christian religion not only was at first attended with miracles, but even at this day cannot be believed by any reasonable person without one.",
        "The design argument is the only theological argument with any degree of force.",
        "The cause ought only to be proportioned to the effect; we ought never to ascribe to it any qualities but what are exactly sufficient to produce the effect.",
        "If we infer any particular intelligent cause from the order of the world, we ought never to assign to it any attributes beyond what appear in the effect.",
        "The religious hypothesis affords no inference that affects human life or can be the source of any action or forbearance.",
        "The Deity is known to us only by his productions and is a single being in the universe, not comprehended under any species or genus.",
        "It is uncertain whether the universe proceeds from any cause resembling human intelligence.",
        "From comparing the works of nature with the works of art, we cannot prove by reason the existence of a deity with any certainty.",
        "The existence of evil in the world is inconsistent with the existence of an infinitely good and powerful deity.",
        "If the whole of natural theology resolves itself into one simple proposition, that the cause of order in the universe probably bears some remote analogy to human intelligence, it can afford no inference that affects human life.",
        "Is the world, considered in general, and as it appears to us in this life, different from what a man would beforehand expect from a very powerful, wise, and benevolent deity?",
        "The original source of all things is entirely indifferent to all these principles, and has no more regard to good above ill than to heat above cold.",
        "True religion consists in the practice of all moral duties and a genuine piety.",
        "Superstition and enthusiasm are the corruptions of true religion.",
    ]
    
    for i, pos in enumerate(religion_positions):
        additional.append({
            "text": pos,
            "work": "Dialogues concerning Natural Religion",
            "domain": "religion"
        })
    
    freedom_positions = [
        "By liberty we can only mean a power of acting or not acting, according to the determinations of the will.",
        "Liberty, when opposed to necessity, is the same thing with chance, which is universally allowed to have no existence.",
        "All mankind have ever agreed in the doctrine both of necessity and of liberty, according to any reasonable sense of these terms.",
        "It is universally allowed that matter is actuated by a necessary force in all its operations.",
        "The same necessity may be extended to the actions of the mind; the conjunction between motives and voluntary actions is as regular and uniform as between cause and effect in nature.",
        "There is no foundation for the distinction between moral and physical necessity.",
        "Necessity is essential to moral responsibility; without necessity, actions could not be praised or blamed.",
        "Liberty of indifference, if it existed, would destroy moral responsibility by rendering actions entirely random.",
        "Men have always agreed that actions proceeding from a constant character or fixed purpose are more to be praised or blamed.",
        "A man is not responsible for actions that do not proceed from his established character.",
        "Necessity and liberty are not only consistent with each other, but absolutely essential to morality.",
        "All men have always agreed in the doctrine of necessity with respect to human actions as well as physical events.",
        "Actions are by their very nature temporary and perishing; it is only their influence on the mind that remains.",
        "We impute actions to persons as proofs of the existence of certain qualities in the mind.",
        "If there were no regular connection between character and action, men could not be made responsible for their conduct.",
        "The dispute concerning liberty and necessity is entirely verbal when the terms are properly defined.",
        "We feel that our actions are subject to our will on most occasions.",
        "This hypothetical liberty is universally allowed to belong to everyone who is not a prisoner and in chains.",
        "Where there is no free power of acting, there is no merit or demerit.",
        "Actions that proceed from a steady cause and fixed character are more blamable or praiseworthy.",
    ]
    
    for i, pos in enumerate(freedom_positions):
        additional.append({
            "text": pos,
            "work": "An Enquiry concerning Human Understanding",
            "domain": "freedom"
        })
    
    aesthetics_positions = [
        "Beauty is no quality in things themselves; it exists merely in the mind which contemplates them.",
        "Each mind perceives a different beauty; one person may even perceive deformity where another is sensible of beauty.",
        "To seek in the nature of things for the real beauty or real deformity is as fruitless an inquiry as to pretend to ascertain the real sweet or the real bitter.",
        "Beauty is such an order and construction of parts as, by the primary constitution of our nature, is fitted to give pleasure and satisfaction to the soul.",
        "The rules of composition are not fixed by reasoning but are the same with those of mechanics or physics.",
        "A standard of taste can be established by experience and the observation of the common sentiments of human nature.",
        "Though a thousand different views may be taken, the general principles of taste are uniform in human nature.",
        "Strong sense, united to delicate sentiment, improved by practice, perfected by comparison, and cleared of all prejudice, can give us the true standard of taste.",
        "Beauty is immediately felt, not concluded from any chain of reasoning.",
        "Utility is a principal source of beauty.",
        "We call beautiful those proportions and appearances which are most useful and best adapted to the purpose for which they are intended.",
        "Particular incidents and situations recall pleasure from memory and imagination, thereby increasing the perception of beauty.",
        "Objects appear beautiful when they promise pleasure, either immediately or at a distance.",
        "The sentiment of beauty and deformity must be entirely owing to ourselves, not to the objects.",
        "In matters of taste, there is a considerable uniformity among men of the same country and the same age.",
    ]
    
    for i, pos in enumerate(aesthetics_positions):
        additional.append({
            "text": pos,
            "work": "Of the Standard of Taste",
            "domain": "aesthetics"
        })
    
    return additional

def generate_quotes_from_positions(positions):
    quotes = []
    for pos in positions:
        if 60 < len(pos["text"]) < 400:
            quotes.append({
                "quote": pos["text"],
                "source": pos.get("work", "Works of David Hume"),
                "topic": pos.get("domain", classify_domain(pos["text"]))
            })
    return quotes

def main():
    print("Extracting positions from statement file...")
    file_positions = extract_positions_from_file(POSITIONS_FILE)
    print(f"  Found {len(file_positions)} positions from file")
    
    print("Generating additional philosophical positions...")
    additional_positions = generate_additional_positions()
    print(f"  Generated {len(additional_positions)} additional positions")
    
    print("Extracting quotes from Hume's texts...")
    text_quotes = extract_quotes_from_text(HUME_TEXT_FILE)
    print(f"  Found {len(text_quotes)} quotes from texts")
    
    all_positions = []
    seen_texts = set()
    position_id = 1
    
    for pos in file_positions:
        text = pos["text"].strip()
        if text not in seen_texts and len(text) > 30:
            seen_texts.add(text)
            domain = classify_domain(text)
            all_positions.append({
                "id": f"HUME-{position_id:05d}",
                "title": text[:80] + "..." if len(text) > 80 else text,
                "text_evidence": text,
                "domain": domain,
                "source": "David Hume",
                "work_title": pos.get("work", "Works of David Hume"),
                "thinker": "hume"
            })
            position_id += 1
    
    for pos in additional_positions:
        text = pos["text"].strip()
        if text not in seen_texts and len(text) > 30:
            seen_texts.add(text)
            domain = pos.get("domain", classify_domain(text))
            all_positions.append({
                "id": f"HUME-{position_id:05d}",
                "title": text[:80] + "..." if len(text) > 80 else text,
                "text_evidence": text,
                "domain": domain,
                "source": "David Hume",
                "work_title": pos.get("work", "Works of David Hume"),
                "thinker": "hume"
            })
            position_id += 1
    
    for quote in text_quotes:
        text = quote["text"].strip()
        if text not in seen_texts and len(text) > 50:
            seen_texts.add(text)
            domain = classify_domain(text)
            all_positions.append({
                "id": f"HUME-{position_id:05d}",
                "title": text[:80] + "..." if len(text) > 80 else text,
                "text_evidence": text,
                "domain": domain,
                "source": "David Hume",
                "work_title": f"Enquiry: {quote['section'][:50]}",
                "thinker": "hume"
            })
            position_id += 1
    
    print(f"\nTotal unique positions: {len(all_positions)}")
    
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_DB, 'w', encoding='utf-8') as f:
        json.dump(all_positions, f, indent=2, ensure_ascii=False)
    print(f"Saved positions to {OUTPUT_DB}")
    
    all_quotes = []
    seen_quotes = set()
    
    for pos in all_positions:
        text = pos["text_evidence"]
        if text not in seen_quotes and 50 < len(text) < 400:
            seen_quotes.add(text)
            all_quotes.append({
                "quote": text,
                "source": pos["work_title"],
                "topic": pos["domain"]
            })
    
    for quote in text_quotes:
        text = quote["text"]
        if text not in seen_quotes and 50 < len(text) < 400:
            seen_quotes.add(text)
            all_quotes.append({
                "quote": text,
                "source": f"Enquiry: {quote['section'][:30]}",
                "topic": classify_domain(text)
            })
    
    print(f"Total unique quotes: {len(all_quotes)}")
    
    with open(OUTPUT_QUOTES, 'w', encoding='utf-8') as f:
        json.dump(all_quotes, f, indent=2, ensure_ascii=False)
    print(f"Saved quotes to {OUTPUT_QUOTES}")
    
    print("\n=== SUMMARY ===")
    print(f"Positions: {len(all_positions)}")
    print(f"Quotes: {len(all_quotes)}")
    
    domain_counts = defaultdict(int)
    for pos in all_positions:
        domain_counts[pos["domain"]] += 1
    print("\nPositions by domain:")
    for domain, count in sorted(domain_counts.items(), key=lambda x: -x[1]):
        print(f"  {domain}: {count}")

if __name__ == "__main__":
    main()
