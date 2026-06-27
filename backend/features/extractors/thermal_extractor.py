from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class ThermalExtractor(BaseFeatureExtractor):
    """Extracts thermal parameters from the thermal profile."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        th = product.thermal
        return {
            "peak_temperature": float(th.peak_temperature) if th.peak_temperature is not None else 0.0,
            "emission_measure": float(th.emission_measure) if th.emission_measure is not None else 0.0,
            "heating_rate": float(th.heating_rate) if th.heating_rate is not None else 0.0,
            "cooling_rate": float(th.cooling_rate) if th.cooling_rate is not None else 0.0,
            "thermal_energy": float(th.thermal_energy) if th.thermal_energy is not None else 0.0,
            "temperature_gradient": float(th.temperature_gradient) if th.temperature_gradient is not None else 0.0,
        }
