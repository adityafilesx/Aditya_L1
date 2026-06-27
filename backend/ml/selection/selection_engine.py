import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from backend.ml.registry.model_registry import model_registry, ModelMetadata

class SelectionPolicy(BaseModel):
    policy_id: str
    description: str
    primary_metric: str  # e.g., "mcc", "ece", "balanced_accuracy"
    optimization_direction: str  # "maximize", "minimize"
    weights: Optional[Dict[str, float]] = None # For composite scores
    target_filter: Optional[str] = None # For horizon specific policies

class ModelSelectionEngine:
    """Evaluates and ranks models based on configurable scientific policies."""
    def __init__(self, storage_path: str = "data/ml_selection_policies.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.policies: Dict[str, SelectionPolicy] = {}
        self._load_policies()
        
        # Add default policies if empty
        if not self.policies:
            self.register_policy(SelectionPolicy(
                policy_id="default_highest_mcc",
                description="Highest MCC",
                primary_metric="mcc",
                optimization_direction="maximize"
            ))
            self.register_policy(SelectionPolicy(
                policy_id="default_lowest_ece",
                description="Lowest Expected Calibration Error",
                primary_metric="ece",
                optimization_direction="minimize"
            ))
            self.register_policy(SelectionPolicy(
                policy_id="composite_robustness",
                description="Weighted Composite Score (MCC + F1 - ECE)",
                primary_metric="composite",
                optimization_direction="maximize",
                weights={"mcc": 0.4, "macro_f1": 0.4, "ece": -0.2}
            ))

    def _load_policies(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.policies[k] = SelectionPolicy(**v)
            except Exception:
                self.policies = {}

    def _save_policies(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump({k: v.dict() for k, v in self.policies.items()}, f, indent=2)

    def register_policy(self, policy: SelectionPolicy) -> None:
        self.policies[policy.policy_id] = policy
        self._save_policies()

    def get_policy(self, policy_id: str) -> Optional[SelectionPolicy]:
        return self.policies.get(policy_id)

    def calculate_score(self, model: ModelMetadata, policy_id: str) -> float:
        policy = self.get_policy(policy_id)
        if not policy:
            raise ValueError(f"Policy '{policy_id}' not found.")
            
        metrics = model.evaluation_metrics
        score = 0.0
        
        if policy.primary_metric == "composite" and policy.weights:
            for metric, weight in policy.weights.items():
                val = metrics.get(metric, 0.0)
                score += (val * weight)
        else:
            score = metrics.get(policy.primary_metric, 0.0)
            if policy.optimization_direction == "minimize":
                score = -score  # Invert so higher is always better for sorting
                
        return score

    def rank_models(self, models: List[ModelMetadata], policy_id: str) -> List[ModelMetadata]:
        # Filter models by target if policy specifies one
        policy = self.get_policy(policy_id)
        if policy and policy.target_filter:
            models = [m for m in models if policy.target_filter in m.prediction_targets]
            
        # Calculate scores and store on metadata
        for m in models:
            m.selection_score = self.calculate_score(m, policy_id)
            
        # Sort by score descending
        models.sort(key=lambda m: m.selection_score, reverse=True)
        return models
        
    def select_best_model(self, policy_id: str, candidates_only: bool = True) -> Optional[ModelMetadata]:
        all_models = model_registry.get_all()
        if candidates_only:
            all_models = [m for m in all_models if m.deployment_stage in ["CANDIDATE", "EXPERIMENTAL"]]
            
        if not all_models:
            return None
            
        ranked = self.rank_models(all_models, policy_id)
        return ranked[0] if ranked else None

selection_engine = ModelSelectionEngine()
