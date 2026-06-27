import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class LabelMetadata(BaseModel):
    label_version: str
    target_type: str  # Classification, Regression
    forecast_horizon: str  # e.g., "6hr", "24hr"
    positive_window: str
    negative_window: str
    look_ahead_window: str
    class_distribution: Dict[str, float]
    label_generation_strategy: str
    creation_date: str
    author: str

class LabelManager:
    """Manages label definitions for forecasting and reproducibility."""
    def __init__(self, storage_path: str = "data/ml_labels.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        self.labels: Dict[str, LabelMetadata] = {}
        self._load_labels()

    def _load_labels(self) -> None:
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.labels[k] = LabelMetadata(**v)
            except Exception:
                self.labels = {}

    def _save_labels(self) -> None:
        with open(self.storage_path, "w") as f:
            json.dump({k: v.dict() for k, v in self.labels.items()}, f, indent=2)

    def register_label(self, metadata: LabelMetadata) -> None:
        if metadata.label_version in self.labels:
            raise ValueError(f"Label Version '{metadata.label_version}' already exists.")
        self.labels[metadata.label_version] = metadata
        self._save_labels()

    def get_label(self, label_version: str) -> Optional[LabelMetadata]:
        return self.labels.get(label_version)

    def get_all(self) -> List[LabelMetadata]:
        return list(self.labels.values())

label_manager = LabelManager()
