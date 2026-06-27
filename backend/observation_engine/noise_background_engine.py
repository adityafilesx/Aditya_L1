import random
from .models import NoiseBackgroundResult

class NoiseBackgroundEngine:
    def __init__(self):
        self.version = "1.0.0"
        self.soft_baseline = 1e-8
        self.hard_baseline = 1e-9

    def estimate(self, raw_data: dict) -> NoiseBackgroundResult:
        # Simulate background drift
        self.soft_baseline *= random.uniform(0.999, 1.001)
        self.hard_baseline *= random.uniform(0.999, 1.001)
        
        noise_percentage = random.uniform(1.0, 5.0)
        signal_stability = 100.0 - noise_percentage
        noise_confidence = 1.0 if noise_percentage < 3.0 else 0.8
        
        return NoiseBackgroundResult(
            noise_percentage=noise_percentage,
            signal_stability=signal_stability,
            noise_confidence=noise_confidence,
            soft_xray_background=self.soft_baseline,
            hard_xray_background=self.hard_baseline
        )
