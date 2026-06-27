from typing import Dict, List, Optional
from backend.ml.registry.model_registry import model_registry

class HorizonManager:
    """Manages available models and logic for each specific forecast horizon."""
    
    HORIZONS = ["15m", "30m", "1h", "3h", "6h", "12h", "24h", "7d"]
    
    def __init__(self):
        pass
        
    def get_models_for_horizon(self, horizon: str) -> List[str]:
        """Returns the ACTIVE model IDs for a specific horizon."""
        if horizon not in self.HORIZONS:
            raise ValueError(f"Invalid horizon: {horizon}")
            
        active_models = [m for m in model_registry.get_all() if m.deployment_stage == "ACTIVE"]
        
        horizon_models = [m.model_id for m in active_models if any(horizon in t for t in m.prediction_targets)]
        
        return horizon_models

horizon_manager = HorizonManager()
