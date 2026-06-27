from typing import Dict, List, Optional
from backend.ml.registry.model_registry import model_registry, ModelMetadata
from backend.ml.selection.selection_engine import selection_engine

class LeaderboardManager:
    """Manages the model leaderboard, ranking models separately by prediction target."""
    
    def __init__(self):
        pass
        
    def get_leaderboard(self, target_prediction: str, policy_id: str = "default_highest_mcc", include_experimental: bool = True) -> List[ModelMetadata]:
        all_models = model_registry.get_all()
        
        # Filter models by target prediction
        target_models = [m for m in all_models if target_prediction in m.prediction_targets]
        
        if not include_experimental:
            target_models = [m for m in target_models if m.deployment_stage in ["CANDIDATE", "VALIDATED", "ACTIVE"]]
            
        # Rank models using selection engine
        if target_models:
            target_models = selection_engine.rank_models(target_models, policy_id)
            
        return target_models
        
    def get_all_targets(self) -> List[str]:
        all_models = model_registry.get_all()
        targets = set()
        for m in all_models:
            targets.update(m.prediction_targets)
        return sorted(list(targets))

leaderboard_manager = LeaderboardManager()
