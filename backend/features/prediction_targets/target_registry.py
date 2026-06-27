from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class PredictionTargetSpec(BaseModel):
    target_id: str
    name: str
    description: str
    prediction_window_s: int
    variable_type: str  # "classification" or "regression"
    classes: List[str] = []
    supported_features: List[str] = []
    metric_goals: Dict[str, float] = {}


class PredictionTargetRegistry:
    """Authoritative registry for all downstream forecasting prediction targets."""

    def __init__(self):
        self._targets: Dict[str, PredictionTargetSpec] = {}
        self._bootstrap_targets()

    def register(self, target: PredictionTargetSpec) -> None:
        self._targets[target.target_id] = target

    def get_target(self, target_id: str) -> Optional[PredictionTargetSpec]:
        return self._targets.get(target_id)

    def get_all_targets(self) -> List[PredictionTargetSpec]:
        return list(self._targets.values())

    def _bootstrap_targets(self) -> None:
        # Flare Class probabilities
        windows = [
            ("30m", 1800),
            ("1h", 3600),
            ("6h", 21600),
            ("24h", 86400)
        ]
        for w_name, sec in windows:
            self.register(PredictionTargetSpec(
                target_id=f"T-PROB-{w_name.upper()}",
                name=f"goes_probability_{w_name}",
                description=f"Probability of A/B/C/M/X flare occurrence in next {w_name}",
                prediction_window_s=sec,
                variable_type="classification",
                classes=["A", "B", "C", "M", "X"],
                supported_features=["heating_index", "thermal_dominance", "peak_flux", "peak_temperature"],
                metric_goals={"accuracy": 0.85, "f1_score": 0.80}
            ))

        # Expected parameters
        self.register(PredictionTargetSpec(
            target_id="T-REG-FLUX",
            name="expected_peak_flux",
            description="Regression target for peak flux magnitude",
            prediction_window_s=3600,
            variable_type="regression",
            supported_features=["heating_index", "peak_flux", "maximum_derivative"],
            metric_goals={"rmse": 1e-6}
        ))
        
        self.register(PredictionTargetSpec(
            target_id="T-REG-DURATION",
            name="expected_duration",
            description="Regression target for event duration",
            prediction_window_s=3600,
            variable_type="regression",
            supported_features=["rise_time", "decay_time", "duration", "cooling_rate"],
            metric_goals={"rmse": 300.0}
        ))


# Global singleton instance
target_registry = PredictionTargetRegistry()
