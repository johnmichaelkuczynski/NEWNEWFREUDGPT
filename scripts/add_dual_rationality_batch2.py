#!/usr/bin/env python3
"""
Add Dual Rationality batch 2 positions to the Kuczynski database.
"""

import json
from datetime import datetime

dual_rationality_batch2 = [
    ("Smithian rationality is named after Adam Smith's focus on practical provisioning.", "Smithian Rationality"),
    ("Veblenian rationality is named after Thorstein Veblen's theory of conspicuous consumption.", "Veblenian Rationality"),
    ("The two rationalities have separate evolutionary justifications.", "Dual Rationality"),
    ("Human decision-making processes host both rationalities simultaneously.", "Dual Rationality"),
    ("Smithian logic drives behaviors that ensure survival through efficient resource management.", "Smithian Rationality"),
    ("Veblenian logic drives behaviors that enhance social positioning.", "Veblenian Rationality"),
    ("Economic thought can be reconstructed on this dual foundation.", "Dual Rationality"),
    ("Nuanced economic models must account for both rationalities.", "Dual Rationality"),
    ("Smithian rationality operates across individual and collective levels.", "Smithian Rationality"),
    ("Smithian rationality applies to hunters, entrepreneurs, and household managers alike.", "Smithian Rationality"),
    ("Smithian decisions are based on energy expenditure vs. gain.", "Smithian Rationality"),
    ("The entrepreneur's capital investment decisions are Smithian.", "Smithian Rationality"),
    ("Household budget allocation is an exercise in Smithian rationality.", "Smithian Rationality"),
    ("Smithian thinking prioritizes substance over form.", "Smithian Rationality"),
    ("Smithian rationality is the mindset of those responsible for resource security.", "Smithian Rationality"),
    ("Smithian utility functions allow economists to rank actions.", "Smithian Rationality"),
    ("These functions enable simulation of choice behavior.", "Smithian Rationality"),
    ("They support predictive modeling in market analysis.", "Smithian Rationality"),
    ("Smithian models are limited outside basic economic decision-making.", "Smithian Rationality"),
    ("Smithian models fail in domains like personal relationships or artistic expression.", "Smithian Rationality"),
    ("Smithian rationality adapts to different temporal horizons.", "Smithian Rationality"),
    ("Short-term Smithian behavior values accessibility and quick returns.", "Smithian Rationality"),
    ("Long-term Smithian behavior values sustainability and risk distribution.", "Smithian Rationality"),
    ("Institutional designs reflect Smithian coordination of provisioning.", "Smithian Rationality"),
    ("Governments channel self-interest toward social benefits.", "Smithian Rationality"),
    ("Corporations align labor toward productive ends.", "Smithian Rationality"),
    ("Families allocate roles to maximize collective welfare.", "Smithian Rationality"),
    ("Moral principles can serve as reputation enhancers within Smithian logic.", "Smithian Rationality"),
    ("Religious adherence can function as social insurance.", "Smithian Rationality"),
    ("Political affiliation can coordinate group interests rationally.", "Smithian Rationality"),
    ("Smithian choice involves calculating probabilities and transaction costs.", "Smithian Rationality"),
    ("The essence of Smithian rationality is pursuit of advantage under constraint.", "Smithian Rationality"),
    ("Aesthetic appreciation is not inherently Smithian.", "Smithian Rationality"),
    ("Loyalty and self-sacrifice challenge Smithian reductionism.", "Smithian Rationality"),
    ("Truth-seeking may follow epistemic, not Smithian, rationality.", "Dual Rationality"),
    ("Expanding utility functions too broadly risks theoretical vacuity.", "Dual Rationality"),
    ("The 'contextual activation' hypothesis suggests multiple decision frameworks.", "Dual Rationality"),
    ("The 'substrate' hypothesis posits Smithian calculation as core.", "Dual Rationality"),
    ("Recognizing limits of Smithian rationality is essential for comprehensive understanding.", "Dual Rationality"),
    ("Veblenian value is decoupled from practical utility.", "Veblenian Rationality"),
    ("Conspicuous costliness is a strategic advantage in Veblenian logic.", "Veblenian Rationality"),
    ("Costly signaling is hard to fake, making it a reliable indicator.", "Veblenian Rationality"),
    ("The peacock's tail is a natural example of Veblenian signaling.", "Veblenian Rationality"),
    ("Human parallels include luxury watches and overpriced cocktails.", "Veblenian Rationality"),
    ("Display behaviors are optimized for social, not material, returns.", "Veblenian Rationality"),
    ("Veblenian actors succeed at status maximization.", "Veblenian Rationality"),
    ("Conspicuous consumption functions as social currency.", "Veblenian Rationality"),
    ("Veblen utility inverts traditional economic rationality.", "Veblenian Rationality"),
    ("A $20,000 watch signals access and discernment.", "Veblenian Rationality"),
    ("Positional goods markets are explained by Veblen utility.", "Veblenian Rationality"),
    ("Veblenian display can be overt or sublimated.", "Veblenian Rationality"),
    ("Philanthropy can be a form of prestige purchase.", "Veblenian Rationality"),
    ("Social media curation signals cultural capital.", "Veblenian Rationality"),
    ("Moral stances can act as taste markers.", "Veblenian Rationality"),
    ("Understatement can be a high-status signal.", "Veblenian Rationality"),
    ("Cryptic exclusivity requires insider knowledge.", "Veblenian Rationality"),
    ("What seems wasteful is often investment in mating or dominance economies.", "Veblenian Rationality"),
    ("The billionaire's superyacht is analogous to the peacock's tail.", "Veblenian Rationality"),
    ("Asceticism can be a form of status-through-rejection.", "Veblenian Rationality"),
    ("Desert Fathers used withdrawal as a status currency.", "Veblenian Rationality"),
    ("Artists use obscurity to enhance cultural capital.", "Veblenian Rationality"),
    ("Anti-display is a meta-signal of security.", "Veblenian Rationality"),
    ("Compulsive private consumption challenges signaling theory.", "Veblenian Rationality"),
    ("Self-destructive status competitions may be maladaptive.", "Veblenian Rationality"),
    ("Cultural capital (Bourdieu) determines signaling success.", "Veblenian Rationality"),
    ("Signaling requires calibration to social context.", "Veblenian Rationality"),
    ("Failed signals are often matters of poor timing or cultural misalignment.", "Veblenian Rationality"),
    ("Veblenian logic is powerful but not universal.", "Veblenian Rationality"),
    ("Aesthetic preferences can be exclusivity barriers.", "Veblenian Rationality"),
    ("Religious rituals signal commitment to community.", "Veblenian Rationality"),
    ("Political virtue signaling positions individuals socially.", "Veblenian Rationality"),
    ("Private sacrifice may transcend signaling explanations.", "Veblenian Rationality"),
    ("Gender asymmetries in signaling reflect evolutionary strategies.", "Veblenian Rationality"),
    ("Male display often showcases resource control.", "Veblenian Rationality"),
    ("Female display often emphasizes selectiveness and relational value.", "Veblenian Rationality"),
    ("Veblenian logic is situationally activated, not always 'on.'", "Veblenian Rationality"),
    ("Recognizing signaling motives reframes 'irrational' spending.", "Dual Rationality"),
    ("The $300 sneaker is a teen's investment in social capital.", "Veblenian Rationality"),
    ("The influencer's debt-financed display is a career strategy.", "Veblenian Rationality"),
    ("The artist's rejection of commerce is an authenticity signal.", "Veblenian Rationality"),
    ("Traditional financial advice often misses status incentives.", "Dual Rationality"),
    ("Social mobility efforts often follow Veblenian patterns.", "Veblenian Rationality"),
    ("Rationality must be judged by the actor's goals, not the observer's framework.", "Dual Rationality"),
    ("Internal conflict between rationalities causes genuine irrational outcomes.", "Dual Rationality"),
    ("Entrepreneurs may sacrifice business health for perceived prestige.", "Dual Rationality"),
    ("Academics may chase citations over truth.", "Dual Rationality"),
    ("Consumers may trade financial stability for visible status.", "Dual Rationality"),
    ("Mixed signals reduce effectiveness in both provisioning and display.", "Dual Rationality"),
    ("Digital visibility intensifies rationality collisions.", "Dual Rationality"),
    ("Self-sabotage arises from unresolved contradictions between systems.", "Dual Rationality"),
    ("The Dual OS model sees human minds as multi-code systems.", "Dual Rationality"),
    ("Evolutionary roots explain why the systems conflict.", "Dual Rationality"),
    ("Context determines which system dominates behavior.", "Dual Rationality"),
    ("Economics should model behavior by function, not by abstract rationality.", "Dual Rationality"),
    ("Consumer choice theory must incorporate status motives.", "Dual Rationality"),
    ("Effective policy must address both material and social needs.", "Dual Rationality"),
    ("Cultural trends can be analyzed through display logic.", "Dual Rationality"),
    ("Individuals experience internal tension between saving and signaling.", "Dual Rationality"),
    ("Economics as a science must expand to model dual rationalities.", "Dual Rationality"),
    ("Incomplete models lead to misdiagnosis of human behavior.", "Dual Rationality"),
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
    
    for pos_text, topic in dual_rationality_batch2:
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
    data['database_metadata']['latest_addition'] = f"Dual Rationality Batch 2: +{len(new_positions)} positions"
    
    data['database_metadata']['extraction_batches'].append({
        "batch_number": 16,
        "date": datetime.now().isoformat(),
        "positions_added": len(new_positions),
        "works": [{
            "title": "Dual Rationality in Economics - Batch 2",
            "positions": len(new_positions),
            "topics": ["Smithian Rationality", "Veblenian Rationality", "Dual Rationality"]
        }]
    })
    
    with open(db_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Added {len(new_positions)} Dual Rationality (batch 2) positions.")
    print(f"Total positions: {old_count} -> {len(positions)}")
    print(f"New IDs range: ECON-{max_econ_num+1:03d} to ECON-{counter-1:03d}")

if __name__ == "__main__":
    main()
