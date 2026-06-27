from typing import Dict, Any
from backend.xai.rules.rule_base import rule_base

class ScientificExplanationEngine:
    """Generates physics-based scientific explanations for forecasts across 3 modes."""
    
    def __init__(self):
        pass
        
    def generate_explanation(self, features: Dict[str, Any], predictions: Dict[str, Any], mode: str = "scientific") -> Dict[str, Any]:
        rule_eval = rule_base.evaluate_rules(features, predictions)
        
        heating = features.get("heating_index", 0.0)
        neupert = features.get("neupert_correlation", 0.0)
        
        # Base physical reasoning statements
        statements = []
        if heating > 2.0:
            statements.append("Strong plasma heating detected in active regions.")
        if neupert > 0.7:
            statements.append("Neupert correlation matches typical flare acceleration signatures.")
            
        # Explanations based on modes
        explanation_text = ""
        if mode == "operator":
            explanation_text = "Solar activity indicators suggest potential energy accumulation. "
            if heating > 2.0:
                explanation_text += "Rapid thermal accumulation is underway, indicating an increased risk of solar flares."
            else:
                explanation_text += "The sun remains in a relatively stable state with minimal heating signatures."
        elif mode == "scientific":
            explanation_text = f"Physical parameters: Heating Index={heating:.2f}, Neupert Correlation={neupert:.2f}. "
            explanation_text += " ".join(statements)
        else: # research
            explanation_text = f"Detailed Research Trace: Rules evaluated version={rule_eval['version']}. "
            explanation_text += f"Heating index deviation, Neupert envelope synch, rules score={rule_eval['score']:.2%}. "
            
        return {
            "mode": mode,
            "explanation": explanation_text,
            "rule_evaluation": rule_eval,
            "explanation_confidence": 0.92 if rule_eval["score"] == 1.0 else 0.75
        }

scientific_explanation_engine = ScientificExplanationEngine()
