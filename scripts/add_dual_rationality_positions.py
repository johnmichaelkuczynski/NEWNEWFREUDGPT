#!/usr/bin/env python3
"""
Add Smithian vs Veblenian Dual Rationality positions to the Kuczynski database.
Source: "Dual Rationality in Economics" by J.-M. Kuczynski
"""

import json
from datetime import datetime

dual_rationality_positions = [
    ("Economic behavior is governed by two autonomous rationalities: Smithian and Veblenian.", "Dual Rationality"),
    ("Smithian rationality is focused on provisioning and efficient resource allocation.", "Smithian Rationality"),
    ("Veblenian rationality is centered on status display and social signaling.", "Veblenian Rationality"),
    ("Much apparent economic irrationality is one rationality masquerading as the other.", "Dual Rationality"),
    ("Economic irrationality can also arise from collisions between Smithian and Veblenian rationalities.", "Dual Rationality"),
    ("Luxury purchases are rational under Veblenian logic, not Smithian.", "Veblenian Rationality"),
    ("Extreme frugality may optimize Smithian goals but harm Veblenian social positioning.", "Dual Rationality"),
    ("Smithian rationality is the logic of provisioning.", "Smithian Rationality"),
    ("Smithian rationality aims to maximize returns under constraint.", "Smithian Rationality"),
    ("Returns in Smithian logic can be nutritional, financial, or instrumental.", "Smithian Rationality"),
    ("The Smithian agent is a problem-solver in a world of limited resources.", "Smithian Rationality"),
    ("Smithian rationality values outcomes over appearances.", "Smithian Rationality"),
    ("Smithian rationality is the mindset of the provider.", "Smithian Rationality"),
    ("A Smithian utility function formalizes provisioning logic.", "Smithian Rationality"),
    ("The Smithian utility function maps circumstances and actions to a real number representing 'return.'", "Smithian Rationality"),
    ("The Smithian agent chooses the action that maximizes utility.", "Smithian Rationality"),
    ("Smithian models flatten human motivational complexity.", "Smithian Rationality"),
    ("Smithian rationality varies by time horizon, social context, and scale.", "Smithian Rationality"),
    ("Smithian rationality governs everyday decisions like eating, shopping, and time allocation.", "Smithian Rationality"),
    ("Smithian rationality underpins market dynamics and investment strategies.", "Smithian Rationality"),
    ("Short-term Smithian rationality favors immediacy and liquidity.", "Smithian Rationality"),
    ("Long-term Smithian rationality prioritizes sustainability and compounding.", "Smithian Rationality"),
    ("Institutions (governments, firms, families) are macro expressions of Smithian logic.", "Smithian Rationality"),
    ("Moral commitments can piggyback on Smithian rationality as reputation enhancers.", "Smithian Rationality"),
    ("Smithian rationality is not exhaustive; it does not explain aesthetics, loyalty, or self-sacrifice.", "Smithian Rationality"),
    ("Reductionism—treating all behavior as provisioning—risks collapsing meaningful distinctions.", "Dual Rationality"),
    ("There may be other rationalities: ethical, epistemic, religious.", "Dual Rationality"),
    ("Smithian rationality may be one mode among several, activated contextually.", "Dual Rationality"),
    ("Veblenian rationality is the logic of display.", "Veblenian Rationality"),
    ("Veblenian rationality governs signaling of reproductive fitness, social dominance, or cultural superiority.", "Veblenian Rationality"),
    ("Value in Veblenian logic lies in visibility, costliness, and perceived extravagance.", "Veblenian Rationality"),
    ("In Veblenian logic, waste becomes a feature—it signals resource abundance.", "Veblenian Rationality"),
    ("Examples of Veblenian display: peacock's tail, luxury watch, overpriced cocktail, gallery opening.", "Veblenian Rationality"),
    ("Veblenian behavior is often mistaken for irrationality in Smithian models.", "Dual Rationality"),
    ("Veblenian behavior is coherent from the standpoint of mate attraction or status consolidation.", "Veblenian Rationality"),
    ("A Veblen utility function assigns value based on perceived signaling value.", "Veblenian Rationality"),
    ("The Veblen utility function maps circumstances and actions to a real number representing signaling worth.", "Veblenian Rationality"),
    ("Wastefulness, exclusivity, and hard-to-fake acts score high Veblen utility.", "Veblenian Rationality"),
    ("Veblen utility is relational and positional—depends on audience and cultural coding.", "Veblenian Rationality"),
    ("Veblenian rationality explains luxury consumption, positional goods, and status-seeking.", "Veblenian Rationality"),
    ("Veblenian rationality manifests in blatant luxury spending.", "Veblenian Rationality"),
    ("Veblenian rationality also appears in subtle forms: minimalist architecture, philanthropy, curated social media.", "Veblenian Rationality"),
    ("Virtue can be Veblenized when moral stances become status markers.", "Veblenian Rationality"),
    ("Veblenian displays can be aggressive (bling) or restrained (understated elegance).", "Veblenian Rationality"),
    ("All Veblenian displays serve reproductive or hierarchical functions: to be seen and to position oneself above others.", "Veblenian Rationality"),
    ("Edge case: asceticism as status-through-withdrawal.", "Veblenian Rationality"),
    ("Edge case: artists cultivating obscurity to enhance mystique.", "Veblenian Rationality"),
    ("Some behaviors signal by denying they are signals (anti-display).", "Veblenian Rationality"),
    ("Edge case: compulsive consumption without an audience.", "Veblenian Rationality"),
    ("Edge case: status performances that become self-harm.", "Veblenian Rationality"),
    ("Signal failure: mimicking elite cues without cultural fluency.", "Veblenian Rationality"),
    ("Veblenian efficacy depends on audience recognition, cultural fluency, and timing.", "Veblenian Rationality"),
    ("Veblenian rationality extends to art, religion, politics, and self-denial.", "Veblenian Rationality"),
    ("Aesthetic choices often double as status markers.", "Veblenian Rationality"),
    ("Religious devotion can function as display of costly commitment.", "Veblenian Rationality"),
    ("Political affiliation serves as identity performance.", "Veblenian Rationality"),
    ("Not all such behavior is reducible to signaling (e.g., private sacrifice).", "Veblenian Rationality"),
    ("Veblenian signaling is often gender-asymmetric.", "Veblenian Rationality"),
    ("Male Veblenian signaling emphasizes provisioning/dominance.", "Veblenian Rationality"),
    ("Female Veblenian signaling may emphasize beauty/selectivity/relational leverage.", "Veblenian Rationality"),
    ("Misdiagnosis: Behaviors labeled irrational are often Veblen-rational.", "Dual Rationality"),
    ("Examples of Veblen-rational behavior: $300 sneakers, influencer lifestyles on credit, artists refusing commercial success.", "Veblenian Rationality"),
    ("These are calculated signaling attempts within a social economy.", "Veblenian Rationality"),
    ("Traditional models mislabel signaling as wasteful, neurotic, or self-destructive.", "Dual Rationality"),
    ("Rationality isn't failing—the model of rationality is too narrow.", "Dual Rationality"),
    ("Collisions between Smithian and Veblenian rationalities produce genuine irrationality.", "Dual Rationality"),
    ("Examples of collision: entrepreneur bankrupting for prestige, academic sabotaging research for fashion.", "Dual Rationality"),
    ("Incoherence arises from trying to satisfy two incompatible systems.", "Dual Rationality"),
    ("Smith says conserve; Veblen says burn.", "Dual Rationality"),
    ("The result of collision is behavioral noise: mixed signals and wasted effort.", "Dual Rationality"),
    ("Such collisions are increasingly common in modern consumer society.", "Dual Rationality"),
    ("True irrationality is attempting to be two kinds of rational at once.", "Dual Rationality"),
    ("The economic mind runs on a dual OS: Smithian and Veblenian.", "Dual Rationality"),
    ("These systems are evolutionarily grounded and cognitively separable.", "Dual Rationality"),
    ("Smithian and Veblenian systems are often in conflict.", "Dual Rationality"),
    ("Context determines which rationality is expressed.", "Dual Rationality"),
    ("The dual model moves economics beyond rationality vs. irrationality dichotomy.", "Dual Rationality"),
    ("The dual model reframes behavior by its contextual function.", "Dual Rationality"),
    ("Implications for consumer choice modeling: must include both provisioning and display.", "Dual Rationality"),
    ("Implications for policy design: must account for status concerns.", "Dual Rationality"),
    ("Implications for cultural analysis: explains consumption patterns and fashion cycles.", "Dual Rationality"),
    ("Implications for self-understanding: explains internal tension between acquiring and displaying.", "Dual Rationality"),
    ("Most people are not irrational—they are navigating two rationalities.", "Dual Rationality"),
    ("Economics is incomplete without modeling both Smithian and Veblenian systems.", "Dual Rationality"),
    ("Smithian rationality is the substrate of practical economic decision-making.", "Smithian Rationality"),
    ("Veblenian rationality is the substrate of social and sexual selection dynamics.", "Veblenian Rationality"),
    ("The two systems can operate simultaneously within the same individual.", "Dual Rationality"),
    ("What is efficient in one system may be inefficient in the other.", "Dual Rationality"),
    ("Status signaling can be a rational investment in social or mating capital.", "Veblenian Rationality"),
    ("Display logic often requires waste as proof of resource abundance.", "Veblenian Rationality"),
    ("Cultural capital is necessary for successful Veblenian signaling.", "Veblenian Rationality"),
    ("Signaling strategies can become maladaptive if social context changes.", "Veblenian Rationality"),
    ("Moral and ideological commitments can be co-opted by both rationalities.", "Dual Rationality"),
    ("Economic models that ignore Veblenian motives will mispredict behavior.", "Dual Rationality"),
    ("The Dual OS model sees conflict as inherent, not aberrant.", "Dual Rationality"),
    ("Behavioral economics often mistakes Veblenian behavior for cognitive bias.", "Dual Rationality"),
    ("Understanding both systems improves prediction in marketing, policy, and finance.", "Dual Rationality"),
    ("The tension between provisioning and display is a core human dilemma.", "Dual Rationality"),
    ("Evolutionary psychology supports the separation of these two rationalities.", "Dual Rationality"),
    ("A complete economic science must model the multi-code human mind.", "Dual Rationality"),
]

def main():
    db_path = 'data/KUCZYNSKI_PHILOSOPHICAL_DATABASE_v42_WITH_BATCH11.json'
    
    with open(db_path, 'r') as f:
        data = json.load(f)
    
    positions = data.get('positions', [])
    existing_ids = {p.get('id', '') for p in positions}
    
    max_econ_num = 0
    for pid in existing_ids:
        if pid.startswith('ECON-'):
            try:
                num = int(pid.split('-')[1])
                max_econ_num = max(max_econ_num, num)
            except:
                pass
    
    new_positions = []
    counter = max_econ_num + 1
    
    for pos_text, topic in dual_rationality_positions:
        pos_id = f"ECON-{counter:03d}"
        while pos_id in existing_ids:
            counter += 1
            pos_id = f"ECON-{counter:03d}"
        
        new_positions.append({
            "id": pos_id,
            "position": pos_text,
            "topic": topic,
            "source": "Dual Rationality in Economics - J.-M. Kuczynski",
            "work_id": "WORK-DUAL-RAT",
            "domain": "philosophy_of_economics"
        })
        existing_ids.add(pos_id)
        counter += 1
    
    positions.extend(new_positions)
    data['positions'] = positions
    
    old_count = data['database_metadata'].get('total_positions', 0)
    data['database_metadata']['total_positions'] = len(positions)
    data['database_metadata']['last_updated'] = datetime.now().isoformat()
    data['database_metadata']['latest_addition'] = f"Dual Rationality in Economics: +{len(new_positions)} positions on Smithian/Veblenian rationality"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 15,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Dual Rationality in Economics",
            "positions": len(new_positions),
            "topics": ["Smithian Rationality", "Veblenian Rationality", "Dual Rationality", "Philosophy of Economics"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Dual Rationality positions to the database.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: ECON-{max_econ_num+1:03d} to ECON-{counter-1:03d}")

if __name__ == "__main__":
    main()
