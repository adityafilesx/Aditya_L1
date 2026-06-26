import pandas as pd
import numpy as np
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class TelemetryHealthStatus:
    NOMINAL = "NOMINAL"
    STALE = "STALE"      # Missing data for > 5 mins
    GAP = "GAP"          # Missing data for > 30 mins
    DEGRADED = "DEGRADED" # Too many NaNs or missing key sensors

class TelemetryMonitor:
    def __init__(self, stale_threshold_min=5, gap_threshold_min=30):
        self.stale_threshold = pd.Timedelta(minutes=stale_threshold_min)
        self.gap_threshold = pd.Timedelta(minutes=gap_threshold_min)
        self.last_packet_time = None
        self.status = TelemetryHealthStatus.NOMINAL

    def evaluate(self, current_time: pd.Timestamp, latest_telemetry_time: pd.Timestamp = None, features: dict = None) -> str:
        """
        Evaluate the health of the incoming telemetry stream.
        """
        if not current_time.tzinfo:
            current_time = current_time.replace(tzinfo=timezone.utc)
            
        if latest_telemetry_time is None:
            if self.last_packet_time is None:
                self.status = TelemetryHealthStatus.GAP
                return self.status
            latest_telemetry_time = self.last_packet_time
        else:
            if not latest_telemetry_time.tzinfo:
                latest_telemetry_time = latest_telemetry_time.replace(tzinfo=timezone.utc)
            self.last_packet_time = latest_telemetry_time

        delta = current_time - latest_telemetry_time

        if delta >= self.gap_threshold:
            self.status = TelemetryHealthStatus.GAP
        elif delta >= self.stale_threshold:
            self.status = TelemetryHealthStatus.STALE
        else:
            self.status = TelemetryHealthStatus.NOMINAL

        # Additional check for DEGRADED if features are provided and mostly NaNs
        if self.status == TelemetryHealthStatus.NOMINAL and features is not None:
            nan_count = sum(1 for v in features.values() if pd.isna(v))
            if len(features) > 0 and (nan_count / len(features)) > 0.5:
                self.status = TelemetryHealthStatus.DEGRADED

        return self.status

    def get_status_message(self) -> str:
        if self.status == TelemetryHealthStatus.NOMINAL:
            return "Telemetry nominal."
        elif self.status == TelemetryHealthStatus.STALE:
            return "Telemetry stale. Awaiting next downlink..."
        elif self.status == TelemetryHealthStatus.GAP:
            return "CRITICAL: Telemetry gap > 30 mins. Model inference paused."
        elif self.status == TelemetryHealthStatus.DEGRADED:
            return "Telemetry degraded. Sensor dropouts detected."
        return "Unknown status."
