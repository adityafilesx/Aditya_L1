from typing import Dict, Any
from backend.xai.rules.rule_base import rule_base

class ScientificConsistencyEngine:
    """Validates predictions against physical expectations and raises contradictions."""
    
    def __init__(self):
        pass
        
    def validate_consistency(self, features: Dict[str, Any], predictions: Dict[str, Any]) -> Dict[str, Any]:
        return rule_base.evaluate_rules(features, predictions)

consistency_validator = ScientificConsistencyEngine()
