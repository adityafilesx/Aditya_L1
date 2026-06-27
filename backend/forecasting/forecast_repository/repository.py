from typing import Dict, Any, List

class ForecastRepository:
    """Immutable storage of all generated forecasts."""
    
    def __init__(self):
        self.store = {}
        
    def save_forecast(self, forecast: Dict[str, Any]):
        fid = forecast["forecast_id"]
        self.store[fid] = forecast
        
    def get_forecast(self, forecast_id: str) -> Dict[str, Any]:
        return self.store.get(forecast_id)
        
    def get_all(self) -> List[Dict[str, Any]]:
        return list(self.store.values())

forecast_repository = ForecastRepository()
