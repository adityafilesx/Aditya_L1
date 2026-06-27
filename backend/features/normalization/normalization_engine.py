from typing import Dict, Any, List
from pydantic import BaseModel
from backend.features.registry.feature_registry import feature_registry

class NormalizationMetadata(BaseModel):
    strategy: str
    params: Dict[str, float]
    normalized_value: float
    transformation_version: str = "1.0.0"


class FeatureNormalizationEngine:
    """Performs scaling and standardization transformations on raw features."""

    def __init__(self):
        # Preset reference statistics for Standard/MinMax scaling
        # In a production setting, these are loaded from a model registry
        self._reference_stats = {
            "peak_temperature": {"mean": 15.0, "std": 5.0, "min": 1.0, "max": 100.0},
            "rise_time": {"mean": 300.0, "std": 150.0, "min": 0.0, "max": 10000.0},
            "decay_time": {"mean": 900.0, "std": 450.0, "min": 0.0, "max": 30000.0},
            "duration": {"mean": 1200.0, "std": 600.0, "min": 10.0, "max": 40000.0},
            "peak_flux": {"mean": 1e-5, "std": 1e-4, "min": 1e-9, "max": 1e-2},
            "heating_index": {"mean": 5.0, "std": 3.0, "min": 0.0, "max": 1000.0},
        }

    def normalize(self, name: str, value: float) -> tuple[float, NormalizationMetadata]:
        entry = feature_registry.get_feature(name)
        if not entry or entry.normalization_strategy == "none":
            return value, NormalizationMetadata(strategy="none", params={}, normalized_value=value)

        strategy = entry.normalization_strategy
        stats = self._reference_stats.get(name, {"mean": 0.0, "std": 1.0, "min": 0.0, "max": 1.0})

        if strategy == "minmax":
            val_min = stats.get("min", entry.allowed_range[0])
            val_max = stats.get("max", entry.allowed_range[1])
            denom = (val_max - val_min)
            norm_val = (value - val_min) / denom if denom > 0 else 0.0
            # Clamp between 0.0 and 1.0
            norm_val = max(0.0, min(1.0, norm_val))
            return norm_val, NormalizationMetadata(
                strategy="minmax",
                params={"min": val_min, "max": val_max},
                normalized_value=norm_val
            )

        elif strategy == "standard":
            mean = stats.get("mean", 0.0)
            std = stats.get("std", 1.0)
            norm_val = (value - mean) / std if std > 0 else 0.0
            return norm_val, NormalizationMetadata(
                strategy="standard",
                params={"mean": mean, "std": std},
                normalized_value=norm_val
            )

        return value, NormalizationMetadata(strategy="none", params={}, normalized_value=value)

    def normalize_batch(self, raw_features: Dict[str, float]) -> tuple[Dict[str, float], Dict[str, NormalizationMetadata]]:
        normalized: Dict[str, float] = {}
        metadata: Dict[str, NormalizationMetadata] = {}

        for name, value in raw_features.items():
            norm_val, meta = self.normalize(name, value)
            normalized[name] = norm_val
            metadata[name] = meta

        return normalized, metadata


# Global singleton instance
normalization_engine = FeatureNormalizationEngine()
