import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class DatasetRecord(BaseModel):
    dataset_id: str
    dataset_version: str
    feature_registry_version: str = "1.0.0"
    feature_engineering_version: str = "1.0.0"
    physics_engine_version: str = "1.0.0"
    source_observation_version: str = "1.0.0"
    feature_version: str
    label_version: str
    training_split: float
    validation_split: float
    testing_split: float
    num_samples: int = 0
    feature_count: int = 0
    positive_labels: int = 0
    negative_labels: int = 0
    missing_values: int = 0
    class_distribution: Dict[str, float] = {}
    creation_time: str
    checksum: str
    source: str
    time_window: str
    forecast_horizon: str

class DatasetRegistry:
    """Manages records of all compiled training and validation datasets."""
    def __init__(self, storage_path: str = "data/ml_datasets.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.datasets: Dict[str, DatasetRecord] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.datasets[k] = DatasetRecord(**v)
            except Exception:
                self.datasets = {}

    def _save_registry(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump({k: v.dict() for k, v in self.datasets.items()}, f, indent=2)

    def register_dataset(self, dataset: DatasetRecord) -> None:
        self.datasets[dataset.dataset_id] = dataset
        self._save_registry()

    def get_dataset(self, dataset_id: str) -> Optional[DatasetRecord]:
        return self.datasets.get(dataset_id)

    def get_all(self) -> List[DatasetRecord]:
        return list(self.datasets.values())

# Global dataset registry singleton
dataset_registry = DatasetRegistry()
