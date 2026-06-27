from typing import Dict, Any

class ComparisonEngine:
    """Highlights discrepancies across different horizons, models, or runs."""
    
    def __init__(self):
        pass
        
    def compare_forecasts(self, f1: Dict[str, Any], f2: Dict[str, Any]) -> Dict[str, Any]:
        p1 = f1.get("probabilities", {})
        p2 = f2.get("probabilities", {})
        
        diff = {cls: p1.get(cls, 0.0) - p2.get(cls, 0.0) for cls in ["A", "B", "C", "M", "X"]}
        
        return {
            "forecast_1_id": f1.get("forecast_id"),
            "forecast_2_id": f2.get("forecast_id"),
            "probability_diff": diff,
            "state_diff": f1.get("state") != f2.get("state")
        }

comparison_engine = ComparisonEngine()
