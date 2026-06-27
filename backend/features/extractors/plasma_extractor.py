from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class PlasmaExtractor(BaseFeatureExtractor):
    """Extracts plasma parameters."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        pl = product.plasma
        return {
            "density": float(pl.density) if pl.density is not None else 0.0,
            "pressure": float(pl.pressure) if pl.pressure is not None else 0.0,
            "energy": float(pl.energy) if pl.energy is not None else 0.0,
        }
