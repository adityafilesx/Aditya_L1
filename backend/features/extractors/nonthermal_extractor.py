from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class NonThermalExtractor(BaseFeatureExtractor):
    """Extracts non-thermal parameters (hard X-ray components)."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        nt = product.nonthermal
        return {
            "peak_electron_energy": float(nt.peak_electron_energy) if nt.peak_electron_energy is not None else 0.0,
            "burst_energy": float(nt.burst_energy) if nt.burst_energy is not None else 0.0,
            "hard_xray_energy": float(nt.hard_xray_energy) if nt.hard_xray_energy is not None else 0.0,
            "electron_flux": float(nt.electron_flux) if nt.electron_flux is not None else 0.0,
            "acceleration_duration": float(nt.acceleration_duration) if nt.acceleration_duration is not None else 0.0,
        }
