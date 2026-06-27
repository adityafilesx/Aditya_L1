"""
Physics Orchestration Manager.

Wires together the 5 specific sub-engines (thermal, non-thermal, spectral,
plasma, neupert) and 2 top-level engines (classification, characterization)
into a unified PhysicsCharacterization product. Stores the product in the
repository and returns the generated Physics Product ID.
"""

from __future__ import annotations

from typing import List, Optional

from backend.nowcasting.models import MasterFlareEntry

from backend.physics.models import (
    PhysicsCharacterization,
    PhysicsQuality,
    PhysicsProvenance,
    ComputationStatus,
)
from backend.physics.thermal.engine import ThermalEngine
from backend.physics.nonthermal.engine import NonThermalEngine
from backend.physics.spectral.engine import SpectralEngine
from backend.physics.plasma.engine import PlasmaEngine
from backend.physics.neupert.engine import NeupertEngine
from backend.physics.classification.engine import ClassificationEngine
from backend.physics.characterization.engine import CharacterizationEngine
from backend.physics.indices.engine import IndicesEngine
from backend.physics.repository.physics_repository import physics_repository


class PhysicsManager:
    """Orchestrates physics characterization pipeline."""

    VERSION = "1.0.0"

    def __init__(self):
        self.thermal_engine = ThermalEngine()
        self.nonthermal_engine = NonThermalEngine()
        self.spectral_engine = SpectralEngine()
        self.plasma_engine = PlasmaEngine()
        self.neupert_engine = NeupertEngine()
        self.classification_engine = ClassificationEngine()
        self.characterization_engine = CharacterizationEngine()
        self.indices_engine = IndicesEngine()

    def characterize(
        self,
        entry: MasterFlareEntry,
        solexs_history: List[float],
        helios_history: List[float],
    ) -> str:
        """
        Run all physics engines, store in repository, and return the Physics Product ID.
        """
        # 1. Temporal Characterization
        char_profile, char_quality = self.characterization_engine.characterize(entry, solexs_history)

        # 2. Classification
        class_profile, class_quality = self.classification_engine.classify(
            char_profile.peak_soft_xray_flux, 
            quality_metric=char_quality.snr_adequacy
        )

        # 3. Thermal
        thermal_profile, thermal_quality = self.thermal_engine.characterize(
            entry, solexs_history, helios_history
        )

        # 4. Non-Thermal
        nonthermal_profile, nonthermal_quality = self.nonthermal_engine.characterize(
            entry, helios_history
        )

        # 5. Spectral
        spectral_profile, spectral_quality = self.spectral_engine.characterize(
            entry, solexs_history, helios_history
        )

        # 6. Plasma (depends on thermal/nonthermal)
        plasma_profile = self.plasma_engine.characterize(thermal_profile, nonthermal_profile)

        # 7. Neupert
        neupert_profile, neupert_quality = self.neupert_engine.characterize(
            entry, solexs_history, helios_history
        )

        # 8. Derived Indices
        indices = self.indices_engine.compute(
            thermal=thermal_profile,
            nonthermal=nonthermal_profile,
            spectral=spectral_profile,
            neupert=neupert_profile,
            char=char_profile,
        )

        # Aggregate Quality
        quality_scores = [
            thermal_quality.data_coverage,
            spectral_quality.spectral_coverage,
            neupert_quality.temporal_coverage,
            class_quality.flux_measurement_quality,
            char_quality.timing_precision,
        ]
        overall_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.0
        
        statuses = [
            thermal_quality.computation_status,
            spectral_quality.computation_status,
            neupert_quality.computation_status,
            class_quality.computation_status,
            char_quality.computation_status,
        ]
        overall_status = ComputationStatus.GOOD
        if ComputationStatus.INSUFFICIENT in statuses:
            overall_status = ComputationStatus.INSUFFICIENT
        elif ComputationStatus.DEGRADED in statuses:
            overall_status = ComputationStatus.DEGRADED

        overall_quality = PhysicsQuality(
            thermal=thermal_quality,
            spectral=spectral_quality,
            neupert=neupert_quality,
            classification=class_quality,
            characterization=char_quality,
            overall_quality_score=round(overall_score, 4),
            overall_status=overall_status,
        )

        # Provenance
        provenance = PhysicsProvenance(
            physics_engine_version=self.VERSION,
            thermal_engine_version=self.thermal_engine.VERSION,
            nonthermal_engine_version=self.nonthermal_engine.VERSION,
            spectral_engine_version=self.spectral_engine.VERSION,
            plasma_engine_version=self.plasma_engine.VERSION,
            neupert_engine_version=self.neupert_engine.VERSION,
            classification_engine_version=self.classification_engine.VERSION,
            characterization_engine_version=self.characterization_engine.VERSION,
            indices_engine_version=self.indices_engine.VERSION,
            observation_ids=[], # Future
            detector_versions=[], # Future
            pipeline_version="1.0.0"
        )

        # Assemble Master Product
        product = PhysicsCharacterization(
            master_id=entry.master_id,
            thermal=thermal_profile,
            nonthermal=nonthermal_profile,
            spectral=spectral_profile,
            plasma=plasma_profile,
            neupert=neupert_profile,
            classification=class_profile,
            characterization=char_profile,
            quality=overall_quality,
            indices=indices,
            provenance=provenance,
        )

        # Store and return ID
        physics_product_id = physics_repository.store(product)
        return physics_product_id

# Global instance
physics_manager = PhysicsManager()
