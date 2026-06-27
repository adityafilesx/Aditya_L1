import threading
import time
from typing import Callable, Dict

class ForecastScheduler:
    """Triggers horizon-specific inference at configurable cadences."""
    
    def __init__(self):
        self.cadences_sec = {
            "15m": 60,      # run every 1 minute
            "30m": 5 * 60,  # run every 5 minutes
            "1h": 15 * 60,  # run every 15 mins
            "6h": 60 * 60,  # run every 1 hour
            "24h": 6 * 3600 # run every 6 hours
        }
        self.last_run = {k: 0 for k in self.cadences_sec.keys()}
        self._running = False
        self._thread = None
        self._callback = None

    def start(self, callback: Callable[[str], None]):
        self._callback = callback
        self._running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        
    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            
    def _loop(self):
        while self._running:
            now = time.time()
            for horizon, cadence in self.cadences_sec.items():
                if now - self.last_run[horizon] >= cadence:
                    self.last_run[horizon] = now
                    if self._callback:
                        try:
                            self._callback(horizon)
                        except Exception:
                            pass
            time.sleep(10)

forecast_scheduler = ForecastScheduler()
