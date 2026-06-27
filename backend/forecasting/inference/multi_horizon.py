from typing import Dict, Any
from backend.forecasting.engine.horizon import horizon_manager
from backend.forecasting.inference.probability_engine import probability_engine

class MultiHorizonInference:
    """Orchestrates running separate models independently for each horizon."""
    
    def __init__(self):
        pass
        
    def run_inference(self, features: Dict[str, Any], horizon: str) -> Dict[str, Any]:
        """Runs inference for a specific horizon using its dedicated models."""
        models = horizon_manager.get_models_for_horizon(horizon)
        
        # MOCK: In production, load the specific model from ML engine and run predict()
        # Ensure separate probabilities per horizon
        base_m = 0.01
        if horizon == "15m": base_m = 0.05
        elif horizon == "30m": base_m = 0.10
        elif horizon == "1h": base_m = 0.15
        elif horizon == "6h": base_m = 0.25
        elif horizon == "24h": base_m = 0.40
        
        raw_probs = {
            "A": 0.4,
            "B": 0.3,
            "C": 0.2,
            "M": base_m,
            "X": base_m / 4
        }
        
        final_probs = probability_engine.normalize_probabilities(raw_probs)
        
        return {
            "probabilities": final_probs,
            "horizon": horizon,
            "models_used": models
        }

multi_horizon_inference = MultiHorizonInference()
