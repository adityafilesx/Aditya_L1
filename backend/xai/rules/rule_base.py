from typing import Dict, Any, List

class ScientificRule:
    def __init__(self, rule_id: str, name: str, description: str, check_fn):
        self.rule_id = rule_id
        self.name = name
        self.description = description
        self.check_fn = check_fn

class ScientificRuleBase:
    """Versioned library of physical rules validating flare forecasts."""
    
    VERSION = "1.0.0"
    
    def __init__(self):
        self.rules: List[ScientificRule] = [
            ScientificRule(
                "RULE-001",
                "Thermal Heating Constraint",
                "Heating index must be elevated if X-class probability > 0.3",
                lambda f, p: not (p.get("X", 0.0) > 0.3 and f.get("heating_index", 0.0) < 1.5)
            ),
            ScientificRule(
                "RULE-002",
                "Neupert Effect Sync",
                "High Neupert correlation suggests rapid flux change matching microwave peaks",
                lambda f, p: not (f.get("neupert_correlation", 0.0) > 0.8 and f.get("flux_derivative", 0.0) < 1e-7)
            ),
            ScientificRule(
                "RULE-003",
                "Flux Limit Check",
                "Current flux should match peak predictions within physical limits",
                lambda f, p: f.get("current_flux", 0.0) <= p.get("expected_peak_flux", 1.0)
            )
        ]
        
    def evaluate_rules(self, features: Dict[str, Any], predictions: Dict[str, Any]) -> Dict[str, Any]:
        results = {}
        contradictions = []
        
        for rule in self.rules:
            passed = rule.check_fn(features, predictions)
            results[rule.rule_id] = {
                "name": rule.name,
                "passed": passed,
                "description": rule.description
            }
            if not passed:
                contradictions.append({
                    "rule_id": rule.rule_id,
                    "name": rule.name,
                    "reason": f"Prediction failed constraint: {rule.description}"
                })
                
        return {
            "version": self.VERSION,
            "rule_results": results,
            "contradictions": contradictions,
            "score": sum(1 for r in results.values() if r["passed"]) / len(self.rules)
        }

rule_base = ScientificRuleBase()
