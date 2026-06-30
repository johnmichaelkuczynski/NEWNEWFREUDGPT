#!/usr/bin/env python3
"""
Add 200 Socrates/Plato positions to the Kuczynski database.
Source: Why Was Socrates Executed? analysis
"""

import json
from datetime import datetime

positions_batch1 = [
    ("Socrates was not executed for 'red-pilling' Athenians but for 'blue-pilling' them with confusing sophistries.", "Socrates' Execution"),
    ("Socrates' discussions were seen as agit-prop during a civil war.", "Socrates' Execution"),
    ("Socrates weakened Athenian patriotism by causing citizens to question moral beliefs.", "Socrates' Execution"),
    ("Socrates was disruptive, not necessarily false, in his teachings.", "Socrates' Execution"),
    ("Truths taken out of context can be as damaging as falsehoods.", "Philosophy of Truth"),
    ("Society requires some positions to be uncritically accepted for day-to-day functioning.", "Political Philosophy"),
    ("Socrates targeted those accepted positions, leading to his execution.", "Socrates' Execution"),
    ("The Cave Allegory can be read as a metaphysical hypothesis about reality.", "Plato's Cave Allegory"),
    ("The Cave Allegory can also be read as social commentary about propaganda and illusion.", "Plato's Cave Allegory"),
    ("Plato suggests senses give raw data, but intellect reveals true structure.", "Plato's Epistemology"),
    ("The Cave allegory implies society lives based on lies.", "Plato's Cave Allegory"),
    ("Terms like 'prisoner' and 'shackles' in the Cave suggest a critique of social control.", "Plato's Cave Allegory"),
    ("Plato distrusted both rulers and non-rulers.", "Plato's Political Philosophy"),
    ("The Cave allegory has both epistemological and political interpretations.", "Plato's Cave Allegory"),
    ("Anything in spacetime is an instance of a non-spatiotemporal Form.", "Plato's Theory of Forms"),
    ("Properties (Forms) exist independently of their instances.", "Plato's Theory of Forms"),
    ("The statement 'John and Bill are both tall' presupposes the property of tallness.", "Plato's Theory of Forms"),
    ("Properties cannot be reduced to their instances.", "Plato's Theory of Forms"),
    ("A property is not identical to a scattered object of all its instances.", "Plato's Theory of Forms"),
    ("Properties do not resemble their instances.", "Plato's Theory of Forms"),
    ("Forms are non-spatiotemporal and do not causally interact with instances.", "Plato's Theory of Forms"),
    ("Plato's Theory of Forms is essentially correct.", "Plato's Theory of Forms"),
    ("Properties are 'ways things can be,' not physical entities.", "Plato's Theory of Forms"),
    ("Plato mischaracterized his own theory by assuming resemblance between Forms and instances.", "Plato's Theory of Forms"),
    ("For Plato, justice means 'staying in one's rightful place.'", "Plato's Republic"),
    ("Social position should be determined by innate, unchangeable nature according to Plato.", "Plato's Republic"),
    ("Plato's ideal society is rigidly hierarchical.", "Plato's Republic"),
    ("Social barriers must be impenetrable in Plato's ideal state.", "Plato's Republic"),
    ("Private life is illegitimate for Plato; all life should serve the state.", "Plato's Republic"),
    ("Marriages should be arranged by the state for eugenic purposes according to Plato.", "Plato's Republic"),
    ("Reproduction should be controlled by class in Plato's system.", "Plato's Republic"),
    ("There is no private property in Plato's ideal state.", "Plato's Republic"),
    ("Children should be raised communally in Plato's ideal state.", "Plato's Republic"),
    ("The state must lie to maintain social order according to Plato.", "Plato's Republic"),
    ("Plato distinguishes between 'harmless' and 'harmful' state lies, but the distinction collapses.", "Plato's Republic"),
    ("Plato's justice requires mass ignorance and propaganda.", "Plato's Republic"),
    ("Unity of the state is the highest good for Plato.", "Plato's Republic"),
    ("Plato's Republic resembles a Pol Potist bureaucracy.", "Plato's Republic"),
    ("The ruling class must keep the truth hidden from others in Plato's system.", "Plato's Republic"),
    ("Plato's system denies basic personal freedoms.", "Plato's Republic"),
    ("Plato's epistemology reflects his fear of social change.", "Plato's Epistemology"),
    ("Plato identifies as an aristocrat and wants to preserve class distinctions.", "Plato's Political Philosophy"),
    ("The Republic is less about justice and more about designing a stable hierarchy.", "Plato's Republic"),
    ("Plato's rationalism denies reality to the observable world.", "Plato's Epistemology"),
    ("Plato claims only pure thought reveals true reality.", "Plato's Epistemology"),
    ("Plato's view that only thought reveals reality is absurd—observable things are real.", "Plato's Epistemology"),
    ("Plato's epistemology is a coded defense of social stability.", "Plato's Epistemology"),
    ("The 'Good' for Plato equals the 'real,' which really means 'conducive to social stability.'", "Plato's Epistemology"),
    ("Plato's distrust of the senses stems from distrust of social change.", "Plato's Epistemology"),
    ("Plato's epistemology rationalizes aristocratic rule.", "Plato's Epistemology"),
    ("Descartes' epistemology, like Plato's, responds to social unrest.", "Descartes vs. Plato"),
    ("Descartes sought new certainties as Church authority collapsed.", "Descartes vs. Plato"),
    ("Unlike Plato, Descartes accepted change rather than resisting it.", "Descartes vs. Plato"),
    ("Both Plato and Descartes overemphasize thought and underemphasize observation.", "Descartes vs. Plato"),
    ("Plato celebrated the unreality of the observable; Descartes tried to overcome skepticism about it.", "Descartes vs. Plato"),
    ("Descartes' rationalism is less reactionary than Plato's.", "Descartes vs. Plato"),
    ("Philosophy, like OCD, retreats from reality into internal pseudo-reality.", "Philosophy as Psychopathology"),
    ("Philosophy and OCD are both forms of intellectualized impotence.", "Philosophy as Psychopathology"),
    ("The link between OCD and philosophy is a homology, not just an analogy.", "Philosophy as Psychopathology"),
    ("Political philosophers like Plato do not truly engage the world.", "Philosophy as Psychopathology"),
    ("Plato's system is a priori and replaces the world with his thought-world.", "Plato's Epistemology"),
    ("Plato's proposed society is rigid, OCD-like in its protocols.", "Philosophy as Psychopathology"),
    ("Plato advocates extreme punishments for minor violations.", "Plato's Republic"),
    ("The philosopher-king idea is incoherent—societies need doers, not thinkers.", "Plato's Political Philosophy"),
    ("Marx, like Plato, proposed destroying reality for a fabricated alternative.", "Philosophy as Psychopathology"),
    ("Some political philosophers (Locke, Smith, Hume) do engage reality.", "Philosophy as Psychopathology"),
    ("Locke and Hume were empiricists who tried to make philosophy worldly.", "Empiricism"),
    ("Empiricism collapses into skepticism, another form of autistic withdrawal.", "Empiricism"),
    ("Philosophy tends toward autistic retreat from reality.", "Philosophy as Psychopathology"),
    ("Locke and Hume's empiricism led to skepticism about external reality.", "Empiricism"),
    ("Philosophy often fails to engage actual political realities.", "Philosophy as Psychopathology"),
    ("Plato and Marx are paradigmatic of philosophy as escapism.", "Philosophy as Psychopathology"),
    ("Political theory can engage the world, but that is anti-philosophical in spirit.", "Philosophy as Psychopathology"),
    ("Philosophy as a discipline tends toward intellectual detachment.", "Philosophy as Psychopathology"),
    ("Truth must be contextualized to be useful.", "Philosophy of Truth"),
    ("Disruptive truth-telling can be dangerous in times of crisis.", "Philosophy of Truth"),
    ("Hierarchical societies require deception to maintain order.", "Political Philosophy"),
    ("Social stability often depends on uncritical acceptance of norms.", "Political Philosophy"),
    ("Epistemology is often shaped by political anxiety.", "Epistemology"),
    ("Rationalism can be a defense mechanism against change.", "Epistemology"),
    ("The observable world is real, despite philosophical claims to the contrary.", "Metaphysics"),
    ("Properties exist independently of minds.", "Metaphysics"),
    ("Forms are necessary for meaningful discourse.", "Plato's Theory of Forms"),
    ("Plato's Republic is a blueprint for totalitarianism.", "Plato's Republic"),
    ("Justice, for Plato, is about control, not fairness.", "Plato's Republic"),
    ("The state must propagandize to maintain Plato's justice.", "Plato's Republic"),
    ("Plato's ideal state eliminates individuality.", "Plato's Republic"),
    ("Philosophical systems often reflect their authors' social positions.", "Metaphilosophy"),
    ("Empiricism, pushed to its limits, leads to solipsism.", "Empiricism"),
    ("Philosophy risks becoming an exercise in intellectual avoidance.", "Philosophy as Psychopathology"),
    ("Political philosophy can be practical if it engages reality.", "Political Philosophy"),
    ("The Catholic Church's collapse spurred Descartes' search for certainty.", "Descartes vs. Plato"),
    ("Civil war influenced Plato's political and epistemological views.", "Plato's Epistemology"),
    ("Social unrest drives philosophical innovation.", "Metaphilosophy"),
    ("Philosophy can be a form of psychological coping.", "Philosophy as Psychopathology"),
    ("Intellectuals often fear social change.", "Political Philosophy"),
    ("Plato's work is a reaction to Athenian civil strife.", "Plato's Political Philosophy"),
    ("Marx's philosophy led to destructive implementations.", "Philosophy as Psychopathology"),
    ("Locke, Hume, and Smith succeeded because they engaged empirical reality.", "Empiricism"),
    ("Philosophy, as a discipline, tends to resist empirical engagement.", "Metaphilosophy"),
]

positions_batch2 = [
    ("Societal cohesion in times of crisis can require the suppression of disruptive inquiry.", "Philosophy of Truth"),
    ("Philosophical truth-seeking can be socially destructive if not properly contextualized.", "Philosophy of Truth"),
    ("The value of a truth is not absolute but depends on its social and temporal context.", "Philosophy of Truth"),
    ("'Agit-prop' can be a legitimate label for confusing philosophical discourse during war.", "Socrates' Execution"),
    ("A society's survival can depend more on shared conviction than on objective truth.", "Political Philosophy"),
    ("The charge of 'corrupting the youth' against Socrates was essentially correct from a civic stability standpoint.", "Socrates' Execution"),
    ("Intellectual superiority does not grant immunity from social responsibility.", "Political Philosophy"),
    ("The execution of Socrates was a pragmatic, not a philosophical, decision by Athens.", "Socrates' Execution"),
    ("The existence of universals (properties, Forms) is a logical prerequisite for language and predication.", "Plato's Theory of Forms"),
    ("The argument from commonality ('John and Bill are both tall') is a fundamental proof for abstract entities.", "Plato's Theory of Forms"),
    ("Attempts at nominalism (reducing properties to instances) are logically incoherent.", "Plato's Theory of Forms"),
    ("A property cannot be identical to the sum or collection of its instances because the property is unchanging while the collection changes.", "Plato's Theory of Forms"),
    ("The paradoxes in Plato's Parmenides arise from mistakenly spatializing or temporalizing the Forms.", "Plato's Theory of Forms"),
    ("Forms are best understood as possibilities or ways of being, not as ghostly objects.", "Plato's Theory of Forms"),
    ("The non-spatiotemporal nature of Forms explains why they do not causally interact with the physical world.", "Plato's Theory of Forms"),
    ("Plato's error was in attributing a quasi-physical 'resemblance' between Forms and particulars.", "Plato's Theory of Forms"),
    ("The Theory of Forms, properly understood, is a tautological truth about the nature of predication and possibility.", "Plato's Theory of Forms"),
    ("Rejecting the Theory of Forms invalidates the possibility of logical inference and shared concepts.", "Plato's Theory of Forms"),
    ("Plato's definition of justice ('minding one's own business') is a justification for caste immobility.", "Plato's Republic"),
    ("The 'myth of the metals' is a foundational state lie designed to enforce class destiny.", "Plato's Republic"),
    ("Social class, for Plato, is a metaphysical and biological destiny, not a social construct.", "Plato's Republic"),
    ("The ideal state requires the total abolition of the nuclear family and private affections.", "Plato's Republic"),
    ("Communism of property, family, and spouses is necessary to eliminate factionalism and private interest according to Plato.", "Plato's Republic"),
    ("The Guardian class must live in a state of enforced poverty and communal ownership.", "Plato's Republic"),
    ("Eugenic breeding is a core duty of the rulers to maintain the quality of the ruling class.", "Plato's Republic"),
    ("Education in the Republic is not about enlightenment but about rigid conditioning for class role.", "Plato's Republic"),
    ("Music and art must be censored because they can shape the soul in subversive ways.", "Plato's Republic"),
    ("The 'noble lie' is not an exception but the central operating principle of Platonic governance.", "Plato's Republic"),
    ("Unity (homonoia) is the supreme political good, outweighing freedom or individual happiness.", "Plato's Republic"),
    ("Plato's state is inherently totalitarian, leaving no sphere of life outside political control.", "Plato's Republic"),
    ("The Republic is fundamentally a reactionary text aimed at preventing democratic revolution.", "Plato's Republic"),
    ("Plato's distrust of democracy stems from his experience of Athenian instability and the execution of Socrates.", "Plato's Political Philosophy"),
    ("The philosopher-king is a paradox: the contemplative mind is ill-suited for practical rulership.", "Plato's Political Philosophy"),
    ("Plato's system is self-contradictory: it requires wise rulers but establishes a system that prevents the wise from arising naturally.", "Plato's Republic"),
    ("The Laws proposes even more draconian and intrusive control than the Republic.", "Plato's Republic"),
    ("Plato's political vision is a precursor to modern totalitarian ideologies like communism and fascism in its collectivism and control.", "Plato's Republic"),
    ("Plato's radical dichotomy between the intelligible (real) and sensible (unreal) world is politically motivated.", "Plato's Epistemology"),
    ("Plato's depreciation of the senses is a depreciation of the empirical, changing world of social flux.", "Plato's Epistemology"),
    ("The allegory of the Cave, politically decoded, states that ordinary social life is a prison of false consciousness.", "Plato's Cave Allegory"),
    ("'The Good' is politically equivalent to 'that which preserves the aristocratic social order.'", "Plato's Epistemology"),
    ("Plato's rationalism is an intellectual weapon to de-legitimize the evidence of social change and decay.", "Plato's Epistemology"),
    ("By making reality accessible only to philosophers (aristocrats), Plato grants his class epistemological sovereignty.", "Plato's Epistemology"),
    ("The fear of political chaos is transposed into a metaphysical fear of the unreal, shadowy world of becoming.", "Plato's Epistemology"),
    ("Plato's epistemology is not a sincere inquiry into knowledge but an attempt to rationalize his social position.", "Plato's Epistemology"),
    ("The instability of Athenian democracy directly caused Plato's distrust of appearance and change.", "Plato's Political Philosophy"),
    ("In Plato's system, knowledge (episteme) of Forms guarantees right political rule, creating a circular justification for philosopher-kings.", "Plato's Republic"),
    ("Descartes' Meditations were a response to the epistemological crisis caused by the collapse of Scholasticism.", "Descartes vs. Plato"),
    ("Both Plato and Descartes turned to rationalism as a source of certainty amidst intellectual/social upheaval.", "Descartes vs. Plato"),
    ("Descartes' 'methodological doubt' is a more honest and systematic form of skepticism than Plato's blanket dismissal of the senses.", "Descartes vs. Plato"),
    ("Unlike Plato, Descartes seeks to re-establish the reality of the external world (through God), not deny it.", "Descartes vs. Plato"),
    ("Descartes' project is fundamentally modern and forward-looking, seeking new foundations, while Plato's is reactionary.", "Descartes vs. Plato"),
    ("The Cogito is Descartes' attempt to find an individual, internal certainty to replace lost social/religious certainties.", "Descartes vs. Plato"),
    ("Descartes' rationalism, while extreme, is a tool for rebuilding knowledge, not for preserving a social hierarchy.", "Descartes vs. Plato"),
    ("The anxiety underlying Descartes' work is theological and scientific, not primarily political like Plato's.", "Descartes vs. Plato"),
    ("Both Plato and Descartes exemplify how epistemological extremes (rationalism) are often psychological responses to destabilizing change.", "Philosophy as Psychopathology"),
    ("The core activity of philosophy is the construction of self-referential intellectual systems detached from reality.", "Philosophy as Psychopathology"),
    ("Philosophy's detachment from reality is psychologically homologous to OCD's ritualistic thought-patterns.", "Philosophy as Psychopathology"),
    ("Philosophy and OCD are both forms of 'intellectualized impotence'—an inability to act in the world, replaced by complex thought about it.", "Philosophy as Psychopathology"),
    ("Political philosophy is often no exception; it proposes a priori blueprints rather than engaging empirical realities.", "Philosophy as Psychopathology"),
    ("Plato's Republic is a prime example of an autistic political fantasy, meticulously detailed but unmoored from human nature.", "Philosophy as Psychopathology"),
    ("The rigidity and repetitive protocols in Plato's ideal state mirror the rigid rituals of OCD.", "Philosophy as Psychopathology"),
    ("Marx's philosophy similarly involved destroying the complex existing world for a simplistic, fabricated utopia.", "Philosophy as Psychopathology"),
    ("The philosopher-king ideal reveals philosophy's hubris: the belief that pure thinkers can and should rule practical affairs.", "Philosophy as Psychopathology"),
    ("Successful political thinkers (Locke, Smith, Hume) were successful precisely because they ceased to be traditional philosophers and became empirical social scientists.", "Empiricism"),
    ("Locke and Hume's 'empiricizing' project was an attempt to cure philosophy of its autistic tendencies.", "Empiricism"),
    ("Radical empiricism logically leads to solipsism, which is the ultimate autistic withdrawal—into the solitary mind.", "Empiricism"),
    ("Hume's skepticism is the terminus of the empirical attempt to engage the world: it ends in total disengagement.", "Empiricism"),
    ("Philosophy seems trapped in a dilemma: rationalism leads to detachment from the senses, empiricism leads to detachment from the external world.", "Metaphilosophy"),
    ("The discipline of philosophy, in its pure form, is inherently prone to schizoid or avoidant tendencies.", "Philosophy as Psychopathology"),
    ("The drive for absolute certainty, found in both Plato and Descartes, is a neurotic or pathological intellectual trait.", "Philosophy as Psychopathology"),
    ("Much of philosophy's history can be read as a series of elaborate, intellectualized defense mechanisms against uncertainty and change.", "Philosophy as Psychopathology"),
    ("Plato's work is a masterclass in dressing up political prejudice as metaphysical truth.", "Plato's Political Philosophy"),
    ("The Republic is less a philosophical ideal and more a paranoid reaction to democracy.", "Plato's Republic"),
    ("Plato's lasting influence is largely due to the literary power of his myths and allegories, not their logical coherence.", "Plato's Political Philosophy"),
    ("Marx's system was a destructive, a priori fantasy that ignored historical and human complexity.", "Philosophy as Psychopathology"),
    ("Marxist implementation led to catastrophic consequences precisely because it tried to force reality into a philosophical schema.", "Philosophy as Psychopathology"),
    ("The great merit of empiricists (Locke, Hume) was in trying to tether philosophy to observable reality.", "Empiricism"),
    ("Locke and Hume laid the groundwork for modern social science and liberal economics.", "Empiricism"),
    ("The fatal flaw of Locke and Hume was an inadequate theory of inference, leading Hume to untenable skepticism.", "Empiricism"),
    ("Rationalism systematically overvalues deduction and innate ideas while undervaluing sensory experience and induction.", "Epistemology"),
    ("Rationalism often confuses logical consistency with truth about the world.", "Epistemology"),
    ("The failure to properly analyze language leads to metaphysical confusions like misconstruing Forms.", "Philosophy of Language"),
    ("A philosopher's social and historical context is essential for understanding their epistemology.", "Metaphilosophy"),
    ("Epistemology is rarely a pure search for truth; it is often sociology or psychology in disguise.", "Metaphilosophy"),
    ("The history of philosophy is largely a history of intellectuals coping with personal and societal anxiety.", "Metaphilosophy"),
    ("The most durable philosophical contributions are those that engage with practical, empirical problems.", "Metaphilosophy"),
    ("A useful test for a philosophy is its implementability and consequences in the real world.", "Metaphilosophy"),
    ("Philosophical systems that require mass deception or coercion to sustain themselves are morally bankrupt by definition.", "Political Philosophy"),
    ("The quest for a single, unified, a priori system of truth (Plato, Hegel, Marx) is a philosophical pathology.", "Metaphilosophy"),
    ("Healthy thought accepts ambiguity, change, and the limitations of human knowledge.", "Epistemology"),
    ("The proper role of intellect is to model and interpret sensory data, not to replace it as the primary source of knowledge.", "Epistemology"),
    ("Political theory must be based on a realistic, not an idealized or metaphysical, view of human nature.", "Political Philosophy"),
    ("Freedom—including the freedom to err and choose—is a necessary condition for a just society, contra Plato.", "Political Philosophy"),
    ("The 'common sense' view of the world (that rocks and birds are real) is more defensible than most philosophical systems.", "Metaphysics"),
    ("Progress in understanding the world has come from the scientific method, not from pure philosophical speculation.", "Metaphilosophy"),
    ("Philosophy should be subservient to, or merged with, empirical science and practical reason.", "Metaphilosophy"),
    ("Many traditional philosophical 'problems' are pseudo-problems generated by linguistic confusion or psychological need.", "Metaphilosophy"),
    ("Much of Plato's work mistakes analytic truths (about Forms) for synthetic truths about the world.", "Plato's Theory of Forms"),
    ("Conservatism in politics often correlates with rationalism in epistemology; openness to change correlates with empiricism.", "Political Philosophy"),
    ("The ultimate critique of a philosophy is psychoanalytic: uncovering the unconscious drives and fears that generate it.", "Metaphilosophy"),
    ("Intellectual history is a key part of philosophy, as ideas are weapons and defenses in social struggle.", "Metaphilosophy"),
    ("One should be deeply suspicious of any intellectual who claims to have access to a 'higher reality' inaccessible to the masses.", "Epistemology"),
    ("Simplicity and falsifiability are virtues in a theory; complexity and untestability (like Plato's Forms) are often vices.", "Methodology"),
    ("The ethical value of a political system can be judged by the degree of freedom and truth it allows its citizens.", "Political Philosophy"),
    ("Plato's greatest failure was his inability to imagine a good society based on freedom, diversity, and open inquiry.", "Plato's Political Philosophy"),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    
    existing_ids = {p.get('id', '') for p in positions}
    max_num = 0
    for pid in existing_ids:
        if pid.startswith('PLATO-') or pid.startswith('SOC-'):
            try:
                num = int(pid.split('-')[1])
                max_num = max(max_num, num)
            except:
                pass
    
    new_positions = []
    counter = 1
    
    for pos_text, topic in positions_batch1:
        pos_id = f"PLATO-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"PLATO-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "source": "Why Was Socrates Executed? - Kuczynski Analysis",
            "work_id": "WORK-SOCRATES",
            "domain": "history_of_philosophy"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    for pos_text, topic in positions_batch2:
        pos_id = f"PLATO-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"PLATO-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "source": "Why Was Socrates Executed? - Kuczynski Analysis",
            "work_id": "WORK-SOCRATES",
            "domain": "history_of_philosophy"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Socrates/Plato Analysis: +{len(new_positions)} positions on Socrates' execution, Plato's Forms, Republic, and philosophy as psychopathology"
    
    if 'extraction_batches' not in data['database_metadata']:
        data['database_metadata']['extraction_batches'] = []
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 12,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Why Was Socrates Executed? - Analysis",
            "positions": len(new_positions),
            "topics": [
                "Socrates' Execution",
                "Plato's Cave Allegory", 
                "Plato's Theory of Forms",
                "Plato's Republic",
                "Plato's Epistemology",
                "Descartes vs. Plato",
                "Philosophy as Psychopathology",
                "Empiricism"
            ]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} new positions to the database.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: PLATO-001 to PLATO-{counter-1:03d}")

if __name__ == "__main__":
    main()
