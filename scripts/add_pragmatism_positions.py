#!/usr/bin/env python3
"""
Add Kuczynski's Critique of James's Pragmatism positions to the database.
These positions cover truth, knowledge, usefulness, and the pragmatist theory.
"""

import json
from datetime import datetime

pragmatism_positions = [
    {
        "id": "PRAG-0001",
        "position_id": "PRAG-0001",
        "text": "The meaning of a hypothesis lies in its observable consequences. The meaning of a hypothesis-what it says about the world-lies in its observable consequences.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Hypothesis and Observation"
    },
    {
        "id": "PRAG-0002",
        "position_id": "PRAG-0002",
        "text": "The relationship between a hypothesis and its observable consequences is contingent, not analytic. The reason is that the relationship between a hypothesis and its observable consequences is always contingent, never analytic, as it depends on what the operative conditions and causal mechanisms are.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Hypothesis and Observation"
    },
    {
        "id": "PRAG-0003",
        "position_id": "PRAG-0003",
        "text": "Hypotheses and their observable consequences are not equivalent. H is observationally equivalent with O1...On are the observable consequences of H only if certain conditions and certain mechanisms are operative. Given that different conditions and mechanisms might be operative, this means that H and O are not equivalent, observationally or otherwise.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Hypothesis and Observation"
    },
    {
        "id": "PRAG-0004",
        "position_id": "PRAG-0004",
        "text": "One can accept a hypothesis and deny its observable consequences without contradiction. One could, without self-contradiction or incoherence, accept H and deny O.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Hypothesis and Observation"
    },
    {
        "id": "PRAG-0005",
        "position_id": "PRAG-0005",
        "text": "Hypotheses that are observationally equivalent due to natural law are not the same hypothesis. Does this mean that Q and Q* are the same hypothesis? No.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Observational Equivalence"
    },
    {
        "id": "PRAG-0006",
        "position_id": "PRAG-0006",
        "text": "Observational equivalence due to natural law implies different claims about the world. Given the fact that natural law is what guarantees their observational equivalence, it follows that they make different claims about the world.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Observational Equivalence"
    },
    {
        "id": "PRAG-0007",
        "position_id": "PRAG-0007",
        "text": "Knowledge of physics is required to understand the observational equivalence of certain hypotheses. One does have to know the laws of physics to know that Q and Q* are observationally equivalent, since they don't make the very same claim.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Observational Equivalence"
    },
    {
        "id": "PRAG-0008",
        "position_id": "PRAG-0008",
        "text": "Observational equivalence only guarantees actual equivalence when it is analytic. In general, observational equivalence only guarantees actual equivalence when it is built into the very meanings of the claims in question-when, in other words, it is analytic in nature.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Observational Equivalence"
    },
    {
        "id": "PRAG-0009",
        "position_id": "PRAG-0009",
        "text": "Observational equivalence does not support the pragmatist's position when it is a consequence of meaning-equivalence. In such cases, observational equivalence is a mere consequence of meaning-equivalence and therefore does not redound to the credit of the pragmatist's position.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Observational Equivalence"
    },
    {
        "id": "PRAG-0010",
        "position_id": "PRAG-0010",
        "text": "Truth is a property of ideas that agree with reality. Truth, as any dictionary will tell you, is a property of certain of our ideas. It means their 'agreement,' as falsity means their disagreement, with 'reality.'",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Reality"
    },
    {
        "id": "PRAG-0011",
        "position_id": "PRAG-0011",
        "text": "Pragmatists and intellectualists both accept the definition of truth as agreement with reality. Pragmatists and intellectualists both accept this definition as a matter of course.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Reality"
    },
    {
        "id": "PRAG-0012",
        "position_id": "PRAG-0012",
        "text": "Agreement with reality means being guided to or into working touch with it. To 'agree' in the widest sense with a reality, CAN ONLY MEAN TO BE GUIDED EITHER STRAIGHT UP TO IT OR INTO ITS SURROUNDINGS, OR TO BE PUT INTO SUCH WORKING TOUCH WITH IT AS TO HANDLE EITHER IT OR SOMETHING CONNECTED WITH IT BETTER THAN IF WE DISAGREED.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Reality"
    },
    {
        "id": "PRAG-0013",
        "position_id": "PRAG-0013",
        "text": "A true idea allows us to control the world. A true idea is one that allows us to control the world; a false one is one that doesn't.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0014",
        "position_id": "PRAG-0014",
        "text": "James's definitions of pragmatism contain redundancies. This list contains some redundancies, as we will see.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0015",
        "position_id": "PRAG-0015",
        "text": "Each of James's definitions of pragmatism is false but expresses legitimate insights about knowledge. We will find that each of (i)-(v) is false but that they are distorted ways of expressing a number of legitimate insights concerning knowledge and the acquisition thereof.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0016",
        "position_id": "PRAG-0016",
        "text": "Truth is identical with usefulness is a view James holds. Given that truth is identical with usefulness, ideas often gain in usefulness over time.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0017",
        "position_id": "PRAG-0017",
        "text": "Ideas often gain in usefulness over time, rather than having a fixed quantity of usefulness present in them from the beginning.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0018",
        "position_id": "PRAG-0018",
        "text": "Truth happens to an idea. It follows that 'truth' (i.e. usefulness) does indeed happen (i.e. accrue) to an idea.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0019",
        "position_id": "PRAG-0019",
        "text": "The claim that truth is identical with usefulness does not receive independent evidence from the claim that truth happens to an idea. (iv*) merely registers a corollary of the contention that truth is identical with usefulness and does not provide any independent evidence for it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0020",
        "position_id": "PRAG-0020",
        "text": "The claim that truth happens to an idea is refutable for the same reasons as the claims that truth is usefulness. Because (iv*) presupposes that truth is identical with usefulness, it is refutable for the same reasons as (iii) and (iv).",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0021",
        "position_id": "PRAG-0021",
        "text": "Specific truths are instruments for organizing experience according to James. Not only is truth identical with usefulness: specific truths are nothing other than instruments whose purpose is to help organize experience.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Instrumentalism"
    },
    {
        "id": "PRAG-0022",
        "position_id": "PRAG-0022",
        "text": "Categories like knife, army, rock, tree do not represent external realities but ways of organizing experience according to James. The categories in terms of which we experience the world---knife, army, rock, tree, and possibly even persistent object---do not represent external realities but merely embody ways of organizing what would otherwise be an amorphous mass of experience.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Instrumentalism"
    },
    {
        "id": "PRAG-0023",
        "position_id": "PRAG-0023",
        "text": "Truths constructed from categories are to be understood in instrumental, not representational, terms. The 'truths' that are constructed out of these categories are themselves to be understood in instrumental, as opposed to representational, terms.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Instrumentalism"
    },
    {
        "id": "PRAG-0024",
        "position_id": "PRAG-0024",
        "text": "The property of being experience-organizing can be acquired over time by a so-called 'truth.'",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Instrumentalism"
    },
    {
        "id": "PRAG-0025",
        "position_id": "PRAG-0025",
        "text": "Truth is made, not discovered, according to the pragmatist view.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Construction"
    },
    {
        "id": "PRAG-0026",
        "position_id": "PRAG-0026",
        "text": "Knives, forks, nations, economies, and armies are not merely projective constructs because a construct won't be useful unless it tracks objective realities.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Realism vs Instrumentalism"
    },
    {
        "id": "PRAG-0027",
        "position_id": "PRAG-0027",
        "text": "The blade and handle constitute a single object because they form a predictively robust ensemble.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Objects and Prediction"
    },
    {
        "id": "PRAG-0028",
        "position_id": "PRAG-0028",
        "text": "Practical interests require that collective objects have causal and predictive integrity. Those same practical interests wouldn't be well-served unless the collective thereby formed had a certain causal and predictive integrity.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Objects and Prediction"
    },
    {
        "id": "PRAG-0029",
        "position_id": "PRAG-0029",
        "text": "Grouping people into nations and armies and economies is useful because of their dynamic cohesiveness. The reason we find it useful to group people into nations and armies and economies; useful to group bricks into houses; useful to group stars into galaxies; is that such groups have a certain dynamic cohesiveness.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Objects and Prediction"
    },
    {
        "id": "PRAG-0030",
        "position_id": "PRAG-0030",
        "text": "Thermometers and scalpels are not merely 'useful fictions.' It is all very well to say that thermometers and scalpels are but 'useful fictions'-useful ways of grouping together qualia or events. But see how far you get without these so-called fictions.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Realism vs Instrumentalism"
    },
    {
        "id": "PRAG-0031",
        "position_id": "PRAG-0031",
        "text": "Economies and nations actually exist and are not just useful fictions. See how far you get as an investor without assuming the actual existence of economies and nations.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Realism vs Instrumentalism"
    },
    {
        "id": "PRAG-0032",
        "position_id": "PRAG-0032",
        "text": "Useful constructs track actual causal mechanisms. The reason these 'fictions' are useful, it must be stressed, is that they track actual causal mechanisms.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Realism vs Instrumentalism"
    },
    {
        "id": "PRAG-0033",
        "position_id": "PRAG-0033",
        "text": "Nations, people, etc. exist derivatively of more fundamental entities. A better position is to say that nations, people, etc. exist, albeit derivatively of other, more fundamental entities.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHYSICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Derivative Existence"
    },
    {
        "id": "PRAG-0034",
        "position_id": "PRAG-0034",
        "text": "Pragmatism has tremendous value as a description of our knowledge and its acquisition, not of truth per se. Pragmatism has tremendous value-as a description, not of truth per se, but of our knowledge of it-and, more precisely, of our acquisition of that knowledge.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Value of Pragmatism"
    },
    {
        "id": "PRAG-0035",
        "position_id": "PRAG-0035",
        "text": "James' claim that 'Truth happens to an idea' is both opaque and false when taken literally. Taken literally, this is both opaque and false.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0036",
        "position_id": "PRAG-0036",
        "text": "Replacing 'truth' with 'the property of being knowledge' in James' claim makes it prima facie true. Replace 'truth' with 'the property of being knowledge.' This gives us: Ideas acquire the property of being knowledge; i.e., they do not typically start out as knowledge, but they can become knowledge. Unlike the original claim, this is prima facie true.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge vs Truth"
    },
    {
        "id": "PRAG-0037",
        "position_id": "PRAG-0037",
        "text": "A belief may not constitute knowledge when first acquired but becomes increasingly knowledge-constitutive over time. My belief that rabbits are herbivores did not constitute knowledge when, at the age of three, I first acquired it. With the passage of time and the accumulation of experience, that acceptance became increasingly informed and justified and, for that reason, become increasingly knowledge-constitutive.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge Acquisition"
    },
    {
        "id": "PRAG-0038",
        "position_id": "PRAG-0038",
        "text": "Truth per se is discovered, not made.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Construction"
    },
    {
        "id": "PRAG-0039",
        "position_id": "PRAG-0039",
        "text": "Knowledge is made in the sense of generating beliefs that become knowledge. First, it involves the generation of the belief that, once it is sufficiently justified, becomes knowledge.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge vs Truth"
    },
    {
        "id": "PRAG-0040",
        "position_id": "PRAG-0040",
        "text": "Knowledge is made through a process of justification. Second, it involves the aforementioned process of justification.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge vs Truth"
    },
    {
        "id": "PRAG-0041",
        "position_id": "PRAG-0041",
        "text": "Beliefs become knowledge through a process of justification-construction. In general, beliefs become knowledge thanks to a process of justification-construction.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge Acquisition"
    },
    {
        "id": "PRAG-0042",
        "position_id": "PRAG-0042",
        "text": "Knowledge is acquired by being constructed.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge Acquisition"
    },
    {
        "id": "PRAG-0043",
        "position_id": "PRAG-0043",
        "text": "The claim that true ideas are those that we can assimilate and false ones those we cannot is at best a half-truth. If taken literally, this is at best a half-truth, given that there are highly assimilable false ideas and highly non-assimilable true ones.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0044",
        "position_id": "PRAG-0044",
        "text": "The pragmatist's claim that truth is assimilability and falsehood is non-assimilability is false. For an idea to be true is for it to be assimilable, and for an idea to be false is for it to be non-assimilable; i.e., truth is assimilability and falsehood is non-assimilability. This is an outright falsehood.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0045",
        "position_id": "PRAG-0045",
        "text": "Knowledge is assimilated truth, and beliefs become increasingly knowledge-constitutive as they become increasingly grounded.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge Acquisition"
    },
    {
        "id": "PRAG-0046",
        "position_id": "PRAG-0046",
        "text": "The claim that a true idea is one that allows us to control the world incorrectly represents as a virtue of truth what is actually a virtue of our knowledge of it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge vs Truth"
    },
    {
        "id": "PRAG-0047",
        "position_id": "PRAG-0047",
        "text": "Instances of knowledge are ipso facto empowering.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge and Power"
    },
    {
        "id": "PRAG-0048",
        "position_id": "PRAG-0048",
        "text": "Truths are useless unless known. But they are useless unless known-which shows that the property of being power-enhancing belongs not to those truths per se, but to our knowledge of them.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge and Power"
    },
    {
        "id": "PRAG-0049",
        "position_id": "PRAG-0049",
        "text": "It is knowledge, not truth, that is empowering. In other words, it isn't truth that is empowering: it is knowledge.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge and Power"
    },
    {
        "id": "PRAG-0050",
        "position_id": "PRAG-0050",
        "text": "The pragmatist's claim that truth is ipso facto empowering is false, but knowledge is empowering. The false claim, urged by the pragmatist, that the truth is ipso facto empowering corresponds to the true one that knowledge is empowering.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Knowledge and Power"
    },
    {
        "id": "PRAG-0051",
        "position_id": "PRAG-0051",
        "text": "The meaning of a hypothesis lies in its observable consequences is false. (I) is false, since the observable consequences of a given hypothesis are the vector sum both of what that hypothesis says about world and of the subject's relationship to the alleged reality being described.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0052",
        "position_id": "PRAG-0052",
        "text": "Our knowledge of the veracity of a hypothesis is based on its observable consequences. But (i) parallels the true (albeit utterly truistic) claim that our knowledge of the veracity of a given hypothesis is based on its observable consequences.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Hypothesis and Observation"
    },
    {
        "id": "PRAG-0053",
        "position_id": "PRAG-0053",
        "text": "Claims (i)-(v) are ways of combatting an 'intellectualist' conception of knowledge and replacing it with an 'interactionist' or 'operationalist' conception. What (i)-(v) have in common is that they are ways of combatting an 'intellectualist' conception of knowledge and of replacing it with an 'interactionist' or 'operationalist' conception of it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Intellectualism vs Pragmatism"
    },
    {
        "id": "PRAG-0054",
        "position_id": "PRAG-0054",
        "text": "Claims (i)-(v) replace an object-oriented conception of knowledge with an agent-oriented conception. To make a similar point, (i)-(v) replace an object-oriented conception of knowledge with a subject-oriented-or, better, an agent-oriented-conception of knowledge.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Intellectualism vs Pragmatism"
    },
    {
        "id": "PRAG-0055",
        "position_id": "PRAG-0055",
        "text": "The negations of claims (i)-(v) are correct. Each of (iN)-(vN) is correct, as we have seen.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Critique of James"
    },
    {
        "id": "PRAG-0056",
        "position_id": "PRAG-0056",
        "text": "The negations of claims (i)-(v) suggest that knowledge-acquisition is about passively taking in what is out there and doing as little as possible to disrupt it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Classical Epistemology"
    },
    {
        "id": "PRAG-0057",
        "position_id": "PRAG-0057",
        "text": "Classical Epistemology posits that knowledge-acquisition is about taking note of what exists and doing as little as possible to change it. The idea that James is concerned to refute would be as follows: Knowledge-acquisition is about taking note of what exists and therefore doing as little as possible to change it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Classical Epistemology"
    },
    {
        "id": "PRAG-0058",
        "position_id": "PRAG-0058",
        "text": "Actions are mere precursors to having observations.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Classical Epistemology"
    },
    {
        "id": "PRAG-0059",
        "position_id": "PRAG-0059",
        "text": "The scientific process begins with passive observation and therefore when action ends.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Classical Epistemology"
    },
    {
        "id": "PRAG-0060",
        "position_id": "PRAG-0060",
        "text": "Classical Epistemology may be true in a narrow, technical sense.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Classical Epistemology"
    },
    {
        "id": "PRAG-0061",
        "position_id": "PRAG-0061",
        "text": "Intellectual discoveries are made by solving practical problems.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0062",
        "position_id": "PRAG-0062",
        "text": "Much of physics is fallout from attempts to create better weapons and dams.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0063",
        "position_id": "PRAG-0063",
        "text": "Economics was invented as a way of managing the enormous influx into Europe of wealth from the New World.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_ECONOMICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0064",
        "position_id": "PRAG-0064",
        "text": "Anthropology was invented to help Europeans understand, and interact more productively with, the natives of the lands they were colonizing.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0065",
        "position_id": "PRAG-0065",
        "text": "Psychoanalysis was developed in order to solve otherwise unsolvable psychiatric problems.",
        "work": "Critique of James's Pragmatism",
        "domain": "PSYCHOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0066",
        "position_id": "PRAG-0066",
        "text": "Modern epistemology came into existence in the mid-1600s, about the same time as modern physics and engineering.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "History of Knowledge"
    },
    {
        "id": "PRAG-0067",
        "position_id": "PRAG-0067",
        "text": "Church doctrines lost credibility around the same time as the rise of modern science because they were interfering with scientific progress.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "History of Knowledge"
    },
    {
        "id": "PRAG-0068",
        "position_id": "PRAG-0068",
        "text": "With faith-based epistemology no longer possible, philosophers had to come up with new, non-dogmatic-or even anti-dogmatic-epistemologies.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "History of Knowledge"
    },
    {
        "id": "PRAG-0069",
        "position_id": "PRAG-0069",
        "text": "The discipline of logic began in the mid-1800s with George Boole, whose objective was to automate reasoning.",
        "work": "Critique of James's Pragmatism",
        "domain": "LOGIC",
        "category": "Pragmatism Analysis",
        "subcategory": "History of Knowledge"
    },
    {
        "id": "PRAG-0070",
        "position_id": "PRAG-0070",
        "text": "The automation of logic coincided with the automation of physical production.",
        "work": "Critique of James's Pragmatism",
        "domain": "LOGIC",
        "category": "Pragmatism Analysis",
        "subcategory": "History of Knowledge"
    },
    {
        "id": "PRAG-0071",
        "position_id": "PRAG-0071",
        "text": "'Purely theoretical' problems relate to the coherence of discoveries made in solving practical problems.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0072",
        "position_id": "PRAG-0072",
        "text": "Calculus was invented to compute planetary orbits and other ballistics-related problems.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0073",
        "position_id": "PRAG-0073",
        "text": "'Purely theoretical' problems like infinitesimals and fractals were seen as worth solving only because they were needed to validate an enormously useful belief-system.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0074",
        "position_id": "PRAG-0074",
        "text": "'Purely theoretical' knowledge, so far as there is such a thing, tends to be stale and one-dimensional.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0075",
        "position_id": "PRAG-0075",
        "text": "Book knowledge of finance principles proves useless in practical business.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0076",
        "position_id": "PRAG-0076",
        "text": "'Pure theory' tends to concern itself with mere schemata.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0077",
        "position_id": "PRAG-0077",
        "text": "According to James, ideas are true because they are useful, not the other way around.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0078",
        "position_id": "PRAG-0078",
        "text": "The theorems of trigonometry are useful because they are true, not the other way around.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0079",
        "position_id": "PRAG-0079",
        "text": "Truths are learned-and are worth learning-because they are useful.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0080",
        "position_id": "PRAG-0080",
        "text": "Theoretical knowledge should exist as long as it is anchored in practical knowledge. When it ceases to be so anchored, it degenerates into knowledge of empty formalisms or assumes some otherwise degraded form.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0081",
        "position_id": "PRAG-0081",
        "text": "While it is absurd to identify the true with the useful, it is not absurd to so identify the true in so far as it is worth learning.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Usefulness"
    },
    {
        "id": "PRAG-0082",
        "position_id": "PRAG-0082",
        "text": "Truth is objective, but knowledge is a relationship between subject and object-between mind and world-and there is therefore a subjective side to it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Truth and Knowledge"
    },
    {
        "id": "PRAG-0083",
        "position_id": "PRAG-0083",
        "text": "The intellect (i.e., the ability to acquire and organize knowledge) exists, biologically speaking, to help the organism survive and procreate.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Biological Function"
    },
    {
        "id": "PRAG-0084",
        "position_id": "PRAG-0084",
        "text": "In human beings, intellect has to some extent become autonomous.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Biological Function"
    },
    {
        "id": "PRAG-0085",
        "position_id": "PRAG-0085",
        "text": "The applied mathematician is interested in relations among numbers and other mathematical objects because of their possible practical applications.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Pure vs Applied"
    },
    {
        "id": "PRAG-0086",
        "position_id": "PRAG-0086",
        "text": "The pure mathematician is interested in mathematical relations 'for their own sake'; his objective is not to use them, but simply to learn more about them.",
        "work": "Critique of James's Pragmatism",
        "domain": "PHILOSOPHY_OF_SCIENCE",
        "category": "Pragmatism Analysis",
        "subcategory": "Pure vs Applied"
    },
    {
        "id": "PRAG-0087",
        "position_id": "PRAG-0087",
        "text": "The philosopher is interested in ethical truths 'for their own sake,' whereas the jurist is interested in them because of their practical applications.",
        "work": "Critique of James's Pragmatism",
        "domain": "ETHICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Pure vs Applied"
    },
    {
        "id": "PRAG-0088",
        "position_id": "PRAG-0088",
        "text": "The philosopher investigates coherence-relations internal to a dataset that is of interest only because of its practical applications.",
        "work": "Critique of James's Pragmatism",
        "domain": "METAPHILOSOPHY",
        "category": "Pragmatism Analysis",
        "subcategory": "Pure vs Applied"
    },
    {
        "id": "PRAG-0089",
        "position_id": "PRAG-0089",
        "text": "The theoretician is to the practitioner what the martial artist is to the soldier.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0090",
        "position_id": "PRAG-0090",
        "text": "It is the practitioner who determines both what the theoretician is studying and the general lines along which he studies it.",
        "work": "Critique of James's Pragmatism",
        "domain": "EPISTEMOLOGY",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
    {
        "id": "PRAG-0091",
        "position_id": "PRAG-0091",
        "text": "The points about theoreticians and practitioners hold equally for artistic endeavor.",
        "work": "Critique of James's Pragmatism",
        "domain": "AESTHETICS",
        "category": "Pragmatism Analysis",
        "subcategory": "Theory and Practice"
    },
]

def main():
    db_path = "data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json"
    
    with open(db_path, 'r') as f:
        db = json.load(f)
    
    if isinstance(db, dict) and 'positions' in db:
        positions = db['positions']
    elif isinstance(db, list):
        positions = db
    else:
        print("Unexpected database structure")
        return
    
    existing_ids = {p.get('id', p.get('position_id', '')) for p in positions}
    
    new_positions = []
    for pos in pragmatism_positions:
        if pos['id'] not in existing_ids:
            new_positions.append(pos)
    
    print(f"Found {len(new_positions)} new positions to add")
    
    positions.extend(new_positions)
    
    if isinstance(db, dict):
        db['positions'] = positions
        if 'metadata' in db:
            db['metadata']['total_positions'] = len(positions)
            db['metadata']['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            db['metadata']['batch18_expansion'] = "Critique of James's Pragmatism - 91 positions on truth, knowledge, usefulness"
    
    with open(db_path, 'w') as f:
        json.dump(db, f, indent=2)
    
    print(f"Database now has {len(positions)} total positions")
    print("Added 91 positions on Kuczynski's Critique of James's Pragmatism")

if __name__ == "__main__":
    main()
