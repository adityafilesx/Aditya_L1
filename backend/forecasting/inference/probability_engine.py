from typing import Dict
import numpy as np

class ProbabilityEngine:
    """Ensures class probabilities sum to 1 and applies calibration."""
    
    CLASSES = ["A", "B", "C", "M", "X"]
    
    def __init__(self):
        pass
        
    def normalize_probabilities(self, raw_probs: Dict[str, float]) -> Dict[str, float]:
        """Softmax/normalization to ensure probabilities sum to 1.0"""
        total = sum(raw_probs.get(cls, 0.0) for cls in self.CLASSES)
        
        if total == 0:
            return {cls: 0.2 for cls in self.CLASSES}
            
        normalized = {cls: raw_probs.get(cls, 0.0) / total for cls in self.CLASSES}
        return normalized
        
    def apply_calibration(self, probs: Dict[str, float], model_calibration_info: Dict) -> Dict[str, float]:
        # Dummy calibration logic, assuming it's already calibrated in inference
        return probs

probability_engine = ProbabilityEngine()
