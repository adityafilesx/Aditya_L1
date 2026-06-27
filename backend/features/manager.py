from __future__ import annotations

import math
from datetime import datetime
from typing import List, Dict, Any, Optional

from backend.physics.models import PhysicsCharacterization
from backend.features.models import ScientificFeatureVector, FeatureQuality, FeatureProvenance
from backend.features.repository.feature_store import feature_store

# 4.5 Refinement Engines
from backend.features.registry.feature_registry import feature_registry
from backend.features.validation.validation_engine import validation_engine
from backend.features.quality.quality_engine import quality_engine
from backend.features.normalization.normalization_engine import normalization_engine
from backend.features.temporal.temporal_engine import temporal_engine
from backend.features.lineage.lineage_engine import lineage_engine
from backend.features.statistics.statistics_engine import statistics_engine

# Extractors
from backend.features.extractors.temporal_extractor import TemporalExtractor
from backend.features.extractors.thermal_extractor import ThermalExtractor
from backend.features.extractors.nonthermal_extractor import NonThermalExtractor
from backend.features.extractors.categorical_extractor import CategoricalExtractor
from backend.features.extractors.indices_extractor import IndicesExtractor
from backend.features.extractors.spectral_extractor import SpectralExtractor
from backend.features.extractors.plasma_extractor import PlasmaExtractor
from backend.features.extractors.neupert_extractor import NeupertExtractor


class FeatureManager:
    """Orchestrates the feature engineering pipeline with runtime validation, normalization, and quality gating."""

    VERSION = "1.0.0"

    def __init__(self):
        self.extractors = [
            TemporalExtractor(),
            ThermalExtractor(),
            NonThermalExtractor(),
            CategoricalExtractor(),
            IndicesExtractor(),
            SpectralExtractor(),
            PlasmaExtractor(),
            NeupertExtractor(),
        ]
        self._counter: int = 0
        self._date_prefix: str = datetime.utcnow().strftime('%Y%m%d')

    def _generate_id(self) -> str:
        """Generate a unique Feature Vector ID (FT-YYYYMMDD-NNN)."""
        now_date = datetime.utcnow().strftime('%Y%m%d')
        if now_date != self._date_prefix:
            self._date_prefix = now_date
            self._counter = 0
            
        self._counter += 1
        return f"FT-{self._date_prefix}-{self._counter:03d}"

    def extract_features(self, product: PhysicsCharacterization) -> str:
        """Processes a physics characterization product, performs validation and normalization, and stores the feature vector."""
        # 1. Merge raw features from extractors
        raw_features: Dict[str, float] = {}
        for extractor in self.extractors:
            raw_features.update(extractor.extract(product))

        # 2. Runtime Validation
        validation_results = validation_engine.validate_features(raw_features)
        
        # Check if any feature is INVALID
        has_invalid = any(r.status == "INVALID" for r in validation_results.values())
        statistics_engine.record_validation(not has_invalid)
        
        if has_invalid:
            # Reject immediately
            invalid_fields = [k for k, r in validation_results.items() if r.status == "INVALID"]
            raise ValueError(f"Feature vector validation failed due to invalid fields: {', '.join(invalid_fields)}")

        # 3. Normalization Pipeline
        normalized_features, norm_metadata = normalization_engine.normalize_batch(raw_features)
        statistics_engine.record_normalization(True)

        # 4. Temporal Features
        peak_time = product.characterization.peak_time or datetime.utcnow().isoformat()
        temporal_engine.record_flare(peak_time)
        temporal_features = temporal_engine.ingest_tick(
            solexs=product.characterization.peak_soft_xray or 0.0,
            helios=product.characterization.peak_hard_xray or 0.0,
            temp=product.thermal.peak_temperature or 0.0,
            timestamp_str=peak_time
        )

        # 5. Quality Report
        quality_report = quality_engine.calculate_quality(validation_results, peak_time)

        # 6. Generate ID and Provenance
        feature_vector_id = self._generate_id()
        provenance = FeatureProvenance(
            physics_product_version=product.provenance.physics_engine_version,
            physics_product_id=product.physics_product_id,
            master_id=product.master_id,
            feature_pipeline_version=self.VERSION,
        )

        # 7. Lineage Tracking
        lineage_engine.record_lineage(
            feature_vector_id=feature_vector_id,
            master_id=product.master_id,
            physics_product_id=product.physics_product_id,
            observation_ids=product.provenance.observation_ids,
            validation_status="VALID",
            normalization_version="1.0.0",
            timestamp_str=datetime.utcnow().isoformat() + "Z"
        )

        # Legacy quality wrapper
        missing_fields = [k for k, r in validation_results.items() if r.status in ("WARNING", "DEGRADED")]
        legacy_quality = FeatureQuality(
            is_valid_for_ml=quality_report.is_ml_ready,
            missing_features_count=len(missing_fields),
            missing_fields=missing_fields,
            reason="Degraded features present: " + ", ".join(missing_fields) if missing_fields else "All features valid"
        )

        # 8. Create and store vector
        vector = ScientificFeatureVector(
            feature_vector_id=feature_vector_id,
            physics_product_id=product.physics_product_id,
            master_id=product.master_id,
            raw_features=raw_features,
            normalized_features=normalized_features,
            normalization_metadata=norm_metadata,
            temporal_features=temporal_features,
            quality_report=quality_report,
            quality=legacy_quality,
            provenance=provenance,
            **raw_features  # populate legacy flat fields
        )

        feature_store.store(vector)
        
        # Store back-reference in the physics product
        product.feature_vector_id = feature_vector_id

        return feature_vector_id


# Global instance
feature_manager = FeatureManager()
