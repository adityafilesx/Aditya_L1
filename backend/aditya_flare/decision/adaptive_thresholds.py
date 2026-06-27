import logging
from typing import List, Dict, Any
from backend.aditya_flare.config.config_loader import config
from backend.aditya_flare.decision.common import parse_goes_class

logger = logging.getLogger(__name__)

class AdaptiveThresholdEngine:
    """
    Module 2: Adaptive Thresholding
    Dynamically adjusts the probability thresholds for operational states 
    based on the recent background solar activity (baseline flux).
    """
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.recent_flux_history: List[float] = []
        
        # Load baseline static thresholds
        self.base_prob_thresholds = {
            "WATCH": config.op_prob_watch,
            "PRE-ALERT": config.op_prob_pre_alert,
            "ALERT": config.op_prob_alert,
            "HIGH_ALERT": config.op_prob_high_alert,
        }
        
        # Define background flux regimes
        self.flux_regimes = {
            "QUIET": parse_goes_class("B1"),  # Anything below B1 is very quiet
            "ACTIVE": parse_goes_class("C1"), # C-class background
            "SEVERE": parse_goes_class("M1")  # M-class background
        }

    def update_history(self, current_flux: float):
        """Adds the latest flux measurement to the rolling window."""
        self.recent_flux_history.append(current_flux)
        if len(self.recent_flux_history) > self.window_size:
            self.recent_flux_history.pop(0)

    def get_background_flux(self) -> float:
        """Calculates the median background flux over the rolling window."""
        if not self.recent_flux_history:
            return 0.0
        sorted_history = sorted(self.recent_flux_history)
        n = len(sorted_history)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_history[mid - 1] + sorted_history[mid]) / 2.0
        else:
            return sorted_history[mid]

    def compute_adaptive_thresholds(self) -> Dict[str, float]:
        """
        Adjusts thresholds dynamically:
        - During elevated background (ACTIVE/SEVERE), lowers probability thresholds
          so that the system reacts faster to incoming flares.
        - During completely QUIET backgrounds, increases thresholds slightly
          to suppress false alarms.
        """
        bg_flux = self.get_background_flux()
        dynamic_thresholds = self.base_prob_thresholds.copy()
        
        if bg_flux >= self.flux_regimes["SEVERE"]:
            # Extreme background: lower thresholds by 20% to increase sensitivity
            adjustment_factor = 0.80
            regime = "SEVERE"
        elif bg_flux >= self.flux_regimes["ACTIVE"]:
            # Active background: lower thresholds by 10%
            adjustment_factor = 0.90
            regime = "ACTIVE"
        elif bg_flux <= self.flux_regimes["QUIET"] and bg_flux > 0:
            # Very quiet background: raise thresholds slightly by 5% to reduce false alarms
            adjustment_factor = 1.05
            regime = "QUIET"
        else:
            # Nominal background
            adjustment_factor = 1.0
            regime = "NOMINAL"
            
        for state, base_val in dynamic_thresholds.items():
            # Clamp the adjusted value between 0.05 and 0.95
            adjusted_val = max(0.05, min(0.95, base_val * adjustment_factor))
            dynamic_thresholds[state] = adjusted_val
            
        return {
            "thresholds": dynamic_thresholds,
            "regime": regime,
            "background_flux": bg_flux,
            "adjustment_factor": adjustment_factor
        }
