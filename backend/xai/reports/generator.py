from typing import Dict, Any
from backend.xai.feature_importance.scientific_explanation import scientific_explanation_engine
from backend.xai.scientific_reasoning.evidence import scientific_evidence_engine

class ForecastReportEngine:
    """Assembles automated Scientific Forecast Reports supporting Operator, Scientific, and Research modes."""
    
    def __init__(self):
        pass
        
    def generate_report(self, features: Dict[str, Any], predictions: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
        evidence = scientific_evidence_engine.compile_evidence(features, predictions)
        
        op_explanation = scientific_explanation_engine.generate_explanation(features, predictions, mode="operator")
        sci_explanation = scientific_explanation_engine.generate_explanation(features, predictions, mode="scientific")
        res_explanation = scientific_explanation_engine.generate_explanation(features, predictions, mode="research")
        
        return {
            "evidence": evidence,
            "explanations": {
                "operator": op_explanation["explanation"],
                "scientific": sci_explanation["explanation"],
                "research": res_explanation["explanation"]
            },
            "scientific_justification": decision.get("scientific_justification", "")
        }

forecast_report_engine = ForecastReportEngine()
