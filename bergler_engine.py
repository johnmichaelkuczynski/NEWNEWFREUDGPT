import json
import re
from typing import List, Dict

class BerglerInferenceEngine:
    def __init__(self, rules_file='bergler_rules_full.json'):
        """Initialize the Berglerian inference engine with lazy loading"""
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
            print(f"Bergler inference engine loaded: {len(self.rules):,} rules")
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
        activated.sort(key=lambda r: r.get('year', 1950), reverse=True)
        return activated[:max_rules]

    def format_chain(self, fired_rules: List[Dict]) -> str:
        """Format fired rules into Berglerian psychoanalytic chain explanation."""
        self._ensure_loaded()

        if not fired_rules:
            return "No specific Berglerian rules activated. Proceed with general psychoanalytic principles."

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
        """Determine psychoanalytic viewpoint from rule content"""
        premise = rule.get('premise', '').lower()
        conclusion = rule.get('conclusion', '').lower()
        combined = premise + " " + conclusion

        # Oral regression/masochism
        if any(term in combined for term in ['oral', 'masochism', 'psychic masochism', 'injustice collect']):
            return 'oral masochistic'
        # Gambling
        elif any(term in combined for term in ['gambl', 'betting', 'casino', 'risk']):
            return 'gambling neurosis'
        # Writer's block
        elif any(term in combined for term in ['writer', 'block', 'creative', 'inhibition']):
            return 'creative inhibition'
        # Superego
        elif any(term in combined for term in ['superego', 'guilt', 'conscience', 'punishment']):
            return 'superego'
        # Homosexuality (his controversial views)
        elif any(term in combined for term in ['homosexual', 'inversion', 'perversion']):
            return 'libidinal'
        # Defense mechanisms
        elif any(term in combined for term in ['defense', 'denial', 'projection', 'rationalization']):
            return 'defensive'
        # Mother/pre-oedipal
        elif any(term in combined for term in ['mother', 'pre-oedipal', 'breast', 'refusal']):
            return 'pre-oedipal'
        # Neurosis
        elif any(term in combined for term in ['neurosis', 'neurotic', 'symptom', 'conflict']):
            return 'neurotic'
        else:
            return 'psychoanalytic'


engine = None

def get_engine():
    """Get or create singleton inference engine (lazy-loaded)"""
    global engine
    if engine is None:
        engine = BerglerInferenceEngine()
    return engine
    