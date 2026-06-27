"""
Detector Benchmarking Module.

Tracks detector performance, latency, false trigger rates, and stability.
"""

from __future__ import annotations

import time
from typing import Dict, Optional


class DetectorBenchmark:
    """Computes and stores real-time detector performance benchmarks."""

    def __init__(self, detector_name: str):
        self.detector_name = detector_name
        self.start_time = time.time()
        
        self.total_processed_ticks = 0
        self.total_detected_events = 0
        self.total_false_triggers = 0
        self.missed_detections = 0
        
        self.total_processing_latency_ms = 0.0
        self.total_event_duration_s = 0.0
        self.total_confidence_sum = 0.0
        
        self.is_stable = True
        self.consecutive_errors = 0

    def record_tick(self, processing_latency_ms: float, error: bool = False):
        """Record a processing tick."""
        self.total_processed_ticks += 1
        self.total_processing_latency_ms += processing_latency_ms
        
        if error:
            self.consecutive_errors += 1
            if self.consecutive_errors > 3:
                self.is_stable = False
        else:
            self.consecutive_errors = 0
            self.is_stable = True

    def record_event(self, duration_s: float, confidence: float, is_false_trigger: bool = False):
        """Record a completed event."""
        self.total_detected_events += 1
        self.total_event_duration_s += duration_s
        self.total_confidence_sum += confidence
        
        if is_false_trigger:
            self.total_false_triggers += 1

    def record_missed_event(self):
        """Record an event that should have been detected but wasn't."""
        self.missed_detections += 1

    def get_snapshot(self) -> Dict[str, float]:
        """Return a snapshot of current benchmark metrics."""
        uptime = time.time() - self.start_time
        avg_latency = self.total_processing_latency_ms / max(1, self.total_processed_ticks)
        avg_duration = self.total_event_duration_s / max(1, self.total_detected_events)
        avg_confidence = self.total_confidence_sum / max(1, self.total_detected_events)
        
        false_trigger_rate = self.total_false_triggers / max(1, self.total_detected_events)

        return {
            "detector_name": self.detector_name,
            "detection_latency_avg": round(avg_latency, 2),
            "false_trigger_rate": round(false_trigger_rate, 4),
            "stability": 1.0 if self.is_stable else 0.0,
            "avg_confidence": round(avg_confidence, 4),
            "uptime": round(uptime, 1),
            "avg_event_duration": round(avg_duration, 1),
            "missed_detections": self.missed_detections,
            "total_events": self.total_detected_events,
        }
