import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ExperimentMetadata(BaseModel):
    experiment_id: str
    dataset_version: str
    feature_version: str
    target: str
    algorithm: str
    hyperparameters: Dict[str, Any]
    training_time: float
    validation_metrics: Dict[str, Any]
    notes: str
    random_seed: int
    cross_validation_strategy: str

class ExperimentRegistry:
    """Manages records of all scientific training experiments."""
    def __init__(self, storage_path: str = "data/ml_experiments.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.experiments: Dict[str, ExperimentMetadata] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.experiments[k] = ExperimentMetadata(**v)
            except Exception:
                self.experiments = {}

    def _save_registry(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump({k: v.dict() for k, v in self.experiments.items()}, f, indent=2)

    def log_experiment(self, exp: ExperimentMetadata) -> None:
        self.experiments[exp.experiment_id] = exp
        self._save_registry()

    def get_experiment(self, experiment_id: str) -> Optional[ExperimentMetadata]:
        return self.experiments.get(experiment_id)

    def get_all(self) -> List[ExperimentMetadata]:
        return list(self.experiments.values())

# Global experiment registry singleton
experiment_registry = ExperimentRegistry()
