from typing import Dict
from backend.physics.models import PhysicsCharacterization
from backend.features.extractors.base_extractor import BaseFeatureExtractor

class TemporalExtractor(BaseFeatureExtractor):
    """Extracts temporal properties, rates of change, and flux details from the characterization profile."""

    def extract(self, product: PhysicsCharacterization) -> Dict[str, float]:
        char = product.characterization
        return {
            # Temporal
            "rise_time": float(char.rise_time) if char.rise_time is not None else 0.0,
            "decay_time": float(char.decay_time) if char.decay_time is not None else 0.0,
            "duration": float(char.duration) if char.duration is not None else 0.0,
            "heating_duration": float(char.heating_duration) if char.heating_duration is not None else 0.0,
            "cooling_duration": float(char.cooling_duration) if char.cooling_duration is not None else 0.0,
            "maximum_derivative": float(char.maximum_derivative) if char.maximum_derivative is not None else 0.0,
            
            # Flux/Counts
            "peak_flux": float(char.peak_flux) if char.peak_flux is not None else 0.0,
            "integrated_flux": float(char.integrated_flux) if char.integrated_flux is not None else 0.0,
            "peak_hard_xray": float(char.peak_hard_xray) if char.peak_hard_xray is not None else 0.0,
            "peak_soft_xray": float(char.peak_soft_xray) if char.peak_soft_xray is not None else 0.0,
            "signal_to_noise_ratio": float(char.signal_to_noise_ratio) if char.signal_to_noise_ratio is not None else 0.0,
        }
