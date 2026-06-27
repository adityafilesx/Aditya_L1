import time
import threading
from typing import Dict, Any, List

class ForecastExpiryQueue:
    """Manages the transition of forecasts: Active -> Expired -> Verified."""
    
    def __init__(self):
        self.active_forecasts = []
        self.expired_forecasts = []
        self.verified_forecasts = []
        self._running = False
        self._thread = None
        
    def add_forecast(self, forecast: Dict[str, Any]):
        self.active_forecasts.append(forecast)
        
    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            
    def _loop(self):
        while self._running:
            # MOCK expiration logic
            # Move items from active to expired based on timestamp + horizon
            # Then from expired to verified when actuals arrive
            time.sleep(10)
            
expiry_queue = ForecastExpiryQueue()
