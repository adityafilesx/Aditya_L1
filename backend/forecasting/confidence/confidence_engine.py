from typing import Dict, Any

class ConfidenceEngine:
    """Decomposes confidence and computes overall Forecast Quality Score."""
    
    def __init__(self):
        pass
        
    def calculate_confidence(self, context: Dict[str, Any], model_metrics: Dict[str, Any]) -> Dict[str, float]:
        obs_conf = context.get("observation_quality", 0.9)
        phys_conf = 0.85 if context.get("physics_state") != "QUIET" else 0.95
        model_conf = model_metrics.get("mcc", 0.7)
        calib_conf = 1.0 - model_metrics.get("ece", 0.1)
        
        overall_conf = (obs_conf * 0.3) + (phys_conf * 0.2) + (model_conf * 0.3) + (calib_conf * 0.2)
        
        # Forecast Quality Score independent of probability
        quality_score = min(1.0, overall_conf * 1.1)
        
        return {
            "observation_confidence": obs_conf,
            "physics_confidence": phys_conf,
            "model_confidence": model_conf,
            "calibration_confidence": calib_conf,
            "overall_confidence": overall_conf,
            "forecast_quality_score": quality_score
        }

confidence_engine = ConfidenceEngine()
