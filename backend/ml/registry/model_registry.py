import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ModelMetadata(BaseModel):
    model_id: str
    model_name: str
    architecture: str
    algorithm: str
    version: str
    implementation_classification: str = "Reference" # Reference, Experimental, Production
    prediction_targets: List[str] = []
    selection_score: Optional[float] = None
    experiment_id: str = ""
    random_seed: int = 42
    training_dataset_id: str
    feature_version: str
    label_version: str
    training_date: str
    author: str
    git_commit: str
    hyperparameters: Dict[str, Any]
    evaluation_metrics: Dict[str, Any]
    calibration_version: str
    serving_status: str  # "READY", "OFFLINE"
    deployment_stage: str  # "ACTIVE", "VALIDATED", "CANDIDATE", "EXPERIMENTAL", "ARCHIVED"

class ModelRegistry:
    """Manages versioned, immutable records of trained ML models."""
    def __init__(self, storage_path: str = "data/ml_model_registry.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.models: Dict[str, ModelMetadata] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.models[k] = ModelMetadata(**v)
            except Exception:
                self.models = {}

    def _save_registry(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump({k: v.dict() for k, v in self.models.items()}, f, indent=2)

    def register_model(self, metadata: ModelMetadata) -> None:
        """Register a new immutable model record."""
        if metadata.model_id in self.models:
            raise ValueError(f"Model ID '{metadata.model_id}' already exists. Models are immutable.")
        self.models[metadata.model_id] = metadata
        self._save_registry()

    def update_deployment_stage(self, model_id: str, stage: str, override_reference: bool = False) -> None:
        """Transitions deployment stage."""
        if model_id not in self.models:
            raise KeyError(f"Model '{model_id}' not found.")
        if stage not in ["ACTIVE", "VALIDATED", "CANDIDATE", "EXPERIMENTAL", "ARCHIVED"]:
            raise ValueError(f"Invalid deployment stage: {stage}")
        
        model = self.models[model_id]
        if stage == "ACTIVE" and model.implementation_classification == "Reference" and not override_reference:
            raise ValueError(f"Cannot promote Reference Implementation '{model_id}' to ACTIVE without explicit override.")
        
        # If setting this model to ACTIVE, experimental-out any previous active model of same architecture
        if stage == "ACTIVE":
            for m_id, m in self.models.items():
                if m.architecture == model.architecture and m.deployment_stage == "ACTIVE" and m_id != model_id:
                    m.deployment_stage = "EXPERIMENTAL"
                    
        self.models[model_id].deployment_stage = stage
        self._save_registry()

    def get_model(self, model_id: str) -> Optional[ModelMetadata]:
        return self.models.get(model_id)

    def get_all(self) -> List[ModelMetadata]:
        return list(self.models.values())

    def get_active_model(self) -> Optional[ModelMetadata]:
        for model in self.models.values():
            if model.deployment_stage == "ACTIVE":
                return model
        return None

# Global model registry singleton
model_registry = ModelRegistry()
