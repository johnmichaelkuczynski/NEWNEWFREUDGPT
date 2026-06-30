import json
import re
from typing import List, Dict

class NietzscheInferenceEngine:
    def __init__(self, rules_file='nietzsche_rules_full.json'):
        """Initialize the Nietzschean inference engine with lazy loading"""
        self.rules_file = rules_file
        self.rules = None
        self._loaded = False

    def _ensure_loaded(self):
        """Lazy-load rules on first access"""
        if self._loaded:
            return
        try:
            with open(self.rules_file, 'r', encoding='utf-8') as f:
                self.rules = json.load(f)
            print(f"Nietzsche inference engine loaded: {len(self.rules):,} rules")
        except FileNotFoundError:
            print(f"Warning: {self.rules_file} not found. Using empty ruleset.")
            self.rules = []
        self._loaded = True

    def deduce(self, phenomenon: str, max_rules: int = 15) -> List[Dict]:
        """
        Forward-chaining inference over phenomenon.
        Returns list of fired rules with conclusions and metadata.
        """
        self._ensure_loaded()

        if not self.rules:
            return []

        activated = []
        accumulated_text = phenomenon.lower()

        for rule in self.rules:
            premise_pattern = rule.get('premise', '')
            try:
                if re.search(premise_pattern, accumulated_text, re.IGNORECASE):
                    activated.append(rule)
                    conclusion = rule.get('conclusion', '')
                    accumulated_text += " " + conclusion.lower()
            except re.error:
                continue

        # Sort by year (most recent first) if available
        activated.sort(key=lambda r: r.get('year', 1885), reverse=True)
        return activated[:max_rules]

    def format_chain(self, fired_rules: List[Dict]) -> str:
        """Format fired rules into Nietzschean chain explanation."""
        self._ensure_loaded()

        if not fired_rules:
            return "No specific Nietzschean rules activated. Proceed with general perspectivism."

        chain = []
        for rule in fired_rules:
            viewpoint = self._get_viewpoint(rule)
            year = rule.get('year', '')
            year_str = f" ({year})" if year else ""
            chain.append(
                f"From the {viewpoint} viewpoint{year_str}: {rule.get('conclusion', '')}"
            )

        return "\n\n".join(chain)

    def _get_viewpoint(self, rule: Dict) -> str:
        """Determine philosophical viewpoint from rule content"""
        premise = rule.get('premise', '').lower()
        conclusion = rule.get('conclusion', '').lower()
        combined = premise + " " + conclusion

        # Will to Power
        if any(term in combined for term in ['will to power', 'power', 'strength', 'force', 'domination']):
            return 'will to power'
        # Eternal Recurrence
        elif any(term in combined for term in ['eternal recurrence', 'eternal return', 'recur', 'repeat']):
            return 'eternal recurrence'
        # Master/Slave Morality
        elif any(term in combined for term in ['master', 'slave', 'noble', 'herd', 'ressentiment']):
            return 'genealogical'
        # Übermensch
        elif any(term in combined for term in ['übermensch', 'overman', 'superman', 'self-overcoming']):
            return 'self-overcoming'
        # Nihilism
        elif any(term in combined for term in ['nihil', 'nothing', 'meaningless', 'void', 'god is dead']):
            return 'nihilism'
        # Perspectivism
        elif any(term in combined for term in ['perspective', 'interpret', 'viewpoint', 'truth']):
            return 'perspectival'
        # Critique of morality
        elif any(term in combined for term in ['moral', 'good', 'evil', 'virtue', 'value']):
            return 'moral critique'
        # Dionysian/Apollonian
        elif any(term in combined for term in ['dionys', 'apollon', 'tragic', 'art', 'aesthetic']):
            return 'aesthetic'
        # Psychology
        elif any(term in combined for term in ['psycholog', 'instinct', 'drive', 'unconscious']):
            return 'psychological'
        else:
            return 'critical'


engine = None

def get_engine():
    """Get or create singleton inference engine (lazy-loaded)"""
    global engine
    if engine is None:
        engine = NietzscheInferenceEngine()
    return engine
    