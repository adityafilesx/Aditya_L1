import collections
import logging
import numpy as np

logger = logging.getLogger(__name__)

class DriftMonitor:
    def __init__(self, feature_name='hardness_ratio', window_size=1000, drift_threshold=2.0):
        self.feature_name = feature_name
        self.window_size = window_size
        self.drift_threshold = drift_threshold
        self.history = collections.deque(maxlen=window_size)
        
        # Simple baseline (mean, std) assumed from training. In reality, load from config.
        self.baseline_mean = 0.5 
        self.baseline_std = 0.2

    def update(self, features: dict):
        if self.feature_name in features:
            val = features[self.feature_name]
            if not np.isnan(val):
                self.history.append(val)

    def check_drift(self) -> dict:
        """
        Check if the current distribution of the feature deviates significantly from the baseline.
        Returns a dict with drift status.
        """
        if len(self.history) < self.window_size // 4:
            return {"is_drifting": False, "z_score": 0.0, "message": "Insufficient data"}
            
        current_mean = np.mean(self.history)
        
        # Compute a simple Z-score of the current mean against the baseline distribution
        # (Technically, Z of the sample mean would be sqrt(N) larger, but we just want a rough heuristic)
        z_score = abs(current_mean - self.baseline_mean) / (self.baseline_std + 1e-6)
        
        is_drifting = bool(z_score > self.drift_threshold)
        
        if is_drifting:
            logger.warning(f"Model drift detected on {self.feature_name}. Z-score: {z_score:.2f}")
            
        return {
            "is_drifting": is_drifting,
            "z_score": z_score,
            "current_mean": current_mean
        }
