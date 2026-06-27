from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import numpy as np

class TemporalFeatureEngine:
    """Computes rolling temporal statistics and trend indicators across variable windows."""

    def __init__(self, max_buffer_size: int = 3600):
        # List of tuples: (timestamp, solexs_flux, helios_flux, temperature)
        self._history: List[Tuple[float, float, float, float]] = []
        self._max_buffer_size = max_buffer_size
        self._last_flare_time: Optional[float] = None
        self._flare_times: List[float] = []

    def record_flare(self, timestamp_str: str) -> None:
        """Record the timestamp of a completed flare to compute rates."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            t_val = dt.timestamp()
            self._last_flare_time = t_val
            self._flare_times.append(t_val)
            # Prune flare times older than 1 hour
            now = datetime.utcnow().timestamp()
            self._flare_times = [t for t in self._flare_times if now - t <= 3600]
        except:
            pass

    def ingest_tick(self, solexs: float, helios: float, temp: float, timestamp_str: str) -> Dict[str, float]:
        """Ingests a single tick of telemetry/physics data and computes rolling temporal features."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            t_val = dt.timestamp()
        except:
            t_val = datetime.utcnow().timestamp()

        self._history.append((t_val, solexs, helios, temp))
        if len(self._history) > self._max_buffer_size:
            self._history.pop(0)

        now = t_val
        windows = {
            "1m": 60,
            "5m": 300,
            "15m": 900,
            "30m": 1800,
            "60m": 3600,
        }

        features: Dict[str, float] = {}

        # 1. Rolling statistics for SoLEXS, HEL1OS, and Temperature
        for name, duration in windows.items():
            # Filter history to items within the duration window
            sub_history = [item for item in self._history if now - item[0] <= duration]
            if not sub_history:
                sub_history = [(now, solexs, helios, temp)]

            sol_vals = [item[1] for item in sub_history]
            hel_vals = [item[2] for item in sub_history]
            temp_vals = [item[3] for item in sub_history]

            # Computations
            features[f"solexs_flux_roll_mean_{name}"] = float(np.mean(sol_vals))
            features[f"solexs_flux_roll_median_{name}"] = float(np.median(sol_vals))
            features[f"solexs_flux_roll_std_{name}"] = float(np.std(sol_vals))
            features[f"solexs_flux_roll_var_{name}"] = float(np.var(sol_vals))

            features[f"helios_flux_roll_mean_{name}"] = float(np.mean(hel_vals))
            features[f"helios_flux_roll_std_{name}"] = float(np.std(hel_vals))

            features[f"temp_roll_mean_{name}"] = float(np.mean(temp_vals))

        # 2. Flux and Temperature change rates (First & Second Derivatives)
        # We calculate gradient over the last 1 minute (or 5 ticks minimum)
        recent = [item for item in self._history if now - item[0] <= 60]
        if len(recent) > 5:
            # Linear regression slope (gradient)
            x = np.array([item[0] for item in recent])
            y_sol = np.array([item[1] for item in recent])
            y_temp = np.array([item[3] for item in recent])
            
            # Center x to avoid floating point precision issues
            x_centered = x - x[0]
            
            sol_slope = float(np.polyfit(x_centered, y_sol, 1)[0]) if len(np.unique(x)) > 1 else 0.0
            temp_slope = float(np.polyfit(x_centered, y_temp, 1)[0]) if len(np.unique(x)) > 1 else 0.0
            
            features["flux_change_rate"] = sol_slope
            features["temperature_change_rate"] = temp_slope
            
            # Acceleration (rate of change of slope) over last 5m
            recent_5m = [item for item in self._history if now - item[0] <= 300]
            if len(recent_5m) > 15:
                x_5m = np.array([item[0] for item in recent_5m]) - recent_5m[0][0]
                y_sol_5m = np.array([item[1] for item in recent_5m])
                poly_coefs = np.polyfit(x_5m, y_sol_5m, 2)
                # Second derivative of ax^2 + bx + c is 2a
                features["flux_acceleration"] = float(2 * poly_coefs[0])
            else:
                features["flux_acceleration"] = 0.0
        else:
            features["flux_change_rate"] = 0.0
            features["temperature_change_rate"] = 0.0
            features["flux_acceleration"] = 0.0

        # 3. Flare occurrence statistics
        if self._last_flare_time is not None:
            features["time_since_previous_flare"] = float(now - self._last_flare_time)
        else:
            features["time_since_previous_flare"] = -1.0  # Sentinel

        features["flare_rate_1h"] = float(len(self._flare_times))
        features["observation_frequency"] = float(len(recent)) / 60.0  # Ticks per second

        return features


# Global singleton instance
temporal_engine = TemporalFeatureEngine()
