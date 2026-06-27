from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class IndicesExtractor(BaseFeatureExtractor):
    """Extracts derived dimensionless physics indices."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        ind = product.indices
        return {
            "heating_index": float(ind.heating_index) if ind.heating_index is not None else 0.0,
            "cooling_index": float(ind.cooling_index) if ind.cooling_index is not None else 0.0,
            "energy_release_index": float(ind.energy_release_index) if ind.energy_release_index is not None else 0.0,
            "thermal_dominance": float(ind.thermal_dominance) if ind.thermal_dominance is not None else 0.0,
            "neupert_compliance": float(ind.neupert_compliance) if ind.neupert_compliance is not None else 0.0,
            "spectral_hardness": float(ind.spectral_hardness) if ind.spectral_hardness is not None else 0.0,
            "impulsiveness_index": float(ind.impulsiveness_index) if ind.impulsiveness_index is not None else 0.0,
        }
