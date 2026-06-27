from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class SpectralExtractor(BaseFeatureExtractor):
    """Extracts spectral fit parameters."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        sp = product.spectral
        return {
            "thermal_component": float(sp.thermal_component) if sp.thermal_component is not None else 0.0,
            "nonthermal_component": float(sp.nonthermal_component) if sp.nonthermal_component is not None else 0.0,
            "power_law_index": float(sp.power_law_index) if sp.power_law_index is not None else 0.0,
            "goodness_of_fit": float(sp.goodness_of_fit) if sp.goodness_of_fit is not None else 0.0,
        }
