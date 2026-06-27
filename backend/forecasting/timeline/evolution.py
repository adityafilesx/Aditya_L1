from typing import Dict, Any, List

class ForecastEvolution:
    """Tracks the evolution of forecasts over time."""
    
    def __init__(self):
        self.timeline = []
        
    def add_point(self, forecast: Dict[str, Any], confidence: float):
        point = {
            "timestamp": forecast["timestamp"],
            "forecast_id": forecast["forecast_id"],
            "state": forecast["state"],
            "p_m_class": forecast["probabilities"].get("M", 0.0),
            "p_x_class": forecast["probabilities"].get("X", 0.0),
            "confidence": confidence
        }
        self.timeline.append(point)
        
    def get_timeline(self) -> List[Dict[str, Any]]:
        return self.timeline

evolution_tracker = ForecastEvolution()
