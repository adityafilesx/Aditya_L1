from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from backend.features.normalization.normalization_engine import NormalizationMetadata
from backend.features.quality.quality_engine import FeatureQualityReport

class FeatureQuality(BaseModel):
    """Quality gate for machine learning consumption (legacy wrapper)."""
    is_valid_for_ml: bool = True
    missing_features_count: int = 0
    missing_fields: List[str] = []
    reason: str = "All features present and valid"


class FeatureProvenance(BaseModel):
    """Lineage for the generated feature vector."""
    extracted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    feature_pipeline_version: str = "1.0.0"
    physics_product_version: str = "1.0.0"
    physics_product_id: str = ""
    master_id: str = ""


class ScientificFeatureVector(BaseModel):
    """Flat, machine-learning-ready feature vector.

    Contains only primitive numerical fields (floats/ints) and metadata,
    perfectly suited for downstream conversion to numpy arrays or pandas DataFrames.
    """
    # Identifiers
    feature_vector_id: str = ""
    physics_product_id: str = ""
    master_id: str = ""

    # Legacy flat fields for backwards compatibility with earlier code & tests
    rise_time: float = 0.0
    decay_time: float = 0.0
    duration: float = 0.0
    heating_duration: float = 0.0
    cooling_duration: float = 0.0
    maximum_derivative: float = 0.0
    peak_flux: float = 0.0
    integrated_flux: float = 0.0
    peak_hard_xray: float = 0.0
    peak_soft_xray: float = 0.0
    signal_to_noise_ratio: float = 0.0
    peak_temperature: float = 0.0
    emission_measure: float = 0.0
    heating_rate: float = 0.0
    cooling_rate: float = 0.0
    thermal_energy: float = 0.0
    temperature_gradient: float = 0.0
    peak_electron_energy: float = 0.0
    burst_energy: float = 0.0
    hard_xray_energy: float = 0.0
    electron_flux: float = 0.0
    acceleration_duration: float = 0.0
    thermal_component: float = 0.0
    nonthermal_component: float = 0.0
    power_law_index: float = 0.0
    goodness_of_fit: float = 0.0
    density: float = 0.0
    pressure: float = 0.0
    energy: float = 0.0
    neupert_offset: float = 0.0
    neupert_score: float = 0.0
    neupert_consistency: float = 0.0
    neupert_confidence: float = 0.0
    heating_index: float = 0.0
    cooling_index: float = 0.0
    energy_release_index: float = 0.0
    thermal_dominance: float = 0.0
    neupert_compliance: float = 0.0
    spectral_hardness: float = 0.0
    impulsiveness_index: float = 0.0
    goes_class_val: float = 0.0
    plasma_state_val: float = 0.0

    # 4.5 Core Feature Refinements
    raw_features: Dict[str, float] = Field(default_factory=dict)
    normalized_features: Dict[str, float] = Field(default_factory=dict)
    normalization_metadata: Dict[str, NormalizationMetadata] = Field(default_factory=dict)
    temporal_features: Dict[str, float] = Field(default_factory=dict)
    
    # Validation & Quality
    quality_report: Optional[FeatureQualityReport] = None
    quality: FeatureQuality = Field(default_factory=FeatureQuality)
    provenance: FeatureProvenance = Field(default_factory=FeatureProvenance)

    def to_dict(self) -> Dict[str, float]:
        """Convert features into a flat dictionary of numbers, combining flat and temporal features."""
        exclude_keys = {"feature_vector_id", "physics_product_id", "master_id", "quality", "provenance", "raw_features", "normalized_features", "normalization_metadata", "temporal_features", "quality_report"}
        base_dict = {k: v for k, v in self.dict().items() if k not in exclude_keys}
        # Merge temporal features if present
        base_dict.update(self.temporal_features)
        # Merge normalized versions with suffix "_scaled"
        for k, v in self.normalized_features.items():
            base_dict[f"{k}_scaled"] = v
        return base_dict

    def to_flat_list(self) -> List[float]:
        """Convert features to a ordered flat list of floats, matching dictionary sorting."""
        d = self.to_dict()
        return [float(d[k]) for k in sorted(d.keys())]
