import os
import yaml
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

class ConformalPredictor:
    """
    Wraps point-estimate predictions to provide statistically valid
    Inductive Conformal Prediction (ICP) intervals.
    """
    def __init__(self):
        self.config_path = os.path.join("aditya_flare", "calibration", "conformal_config.yaml")
        self.q_threshold = 0.20 # Default fallback
        self.alpha = 0.10
        self._load_config()
        
    def _load_config(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, "r") as f:
                    data = yaml.safe_load(f)
                    self.q_threshold = data.get("q_threshold", self.q_threshold)
                    self.alpha = data.get("alpha", self.alpha)
        except Exception as e:
            logger.error(f"Failed to load conformal config: {e}")
            
    def apply_conformal_bounds(self, probability: float) -> Dict[str, Any]:
        """
        Applies Inductive Conformal Prediction (ICP) bounds to a point probability.
        Returns the lower bound, upper bound, and a confidence flag.
        """
        lower_bound = max(0.0, probability - self.q_threshold)
        upper_bound = min(1.0, probability + self.q_threshold)
        
        # We define a "Low Confidence" state if the conformal interval is too wide.
        # Let's say any interval width > 0.40 is considered low confidence.
        interval_width = upper_bound - lower_bound
        is_confident = bool(interval_width <= 0.40)
        
        return {
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
            "interval_width": interval_width,
            "is_confident": is_confident,
            "confidence_level": 1.0 - self.alpha
        }
