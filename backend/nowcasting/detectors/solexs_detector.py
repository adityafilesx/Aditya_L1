"""
SoLEXS Soft X-ray Flare Detector.

Detects thermal flare evolution by monitoring gradual soft X-ray increases.
Uses an adaptive EMA background, first-derivative analysis, rolling-average
smoothing, and configurable persistence thresholds for state transitions.

State Machine
-------------
IDLE → MONITORING → RISING → ACTIVE → PEAK → DECAY → ENDED

Every transition is timestamped.  On ENDED a complete ``SolexsEvent`` is
emitted with decomposed confidence scores.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from backend.nowcasting.buffers.sliding_buffer import SlidingBuffer
from backend.nowcasting.config import SolexsDetectorConfig, nowcast_config
from backend.nowcasting.models import (
    DetectorState,
    SolexsEvent,
    ConfidenceDecomposition,
    DetectorSnapshot,
)


class SolexsDetector:
    """SoLEXS soft X-ray thermal flare detector with configurable parameters."""

    VERSION = "1.0.0"

    def __init__(self, config: Optional[SolexsDetectorConfig] = None):
        self.config = config or nowcast_config.solexs
        self.buffer = SlidingBuffer(max_size=self.config.buffer_size)

        # State machine
        self._state = DetectorState.IDLE
        self._persistence_counter: int = 0
        self._observation_count: int = 0
        self._events_detected: int = 0

        # Adaptive background (EMA)
        self._background: float = self.config.background_seed
        self._background_locked: bool = False  # freeze background during a flare

        # Peak tracking
        self._peak_flux: float = 0.0
        self._peak_time: Optional[str] = None

        # Current event being built
        self._current_event: Optional[SolexsEvent] = None
        self._start_time: Optional[str] = None

        # Last completed event
        self.last_event: Optional[SolexsEvent] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(self, flux: float, timestamp: str, obs_quality: float = 1.0) -> Optional[SolexsEvent]:
        """Feed one observation.  Returns a completed SolexsEvent if the
        detector transitions to ENDED, otherwise None.
        """
        self.buffer.push(flux, timestamp)
        self._observation_count += 1

        # Update adaptive background only when NOT in an active detection
        if not self._background_locked:
            self._background = self.config.ema_alpha * flux + (1.0 - self.config.ema_alpha) * self._background

        ratio = flux / self._background if self._background > 0 else 0.0
        deriv = self.buffer.derivative(window=self.config.derivative_window)

        completed_event: Optional[SolexsEvent] = None

        # --- State machine ---
        if self._state == DetectorState.IDLE:
            if ratio >= self.config.monitoring_threshold:
                self._persistence_counter += 1
                if self._persistence_counter >= self.config.monitoring_persistence:
                    self._transition(DetectorState.MONITORING, timestamp)
                    self._persistence_counter = 0
            else:
                self._persistence_counter = 0

        elif self._state == DetectorState.MONITORING:
            if ratio >= self.config.rising_threshold and deriv > 0:
                self._persistence_counter += 1
                if self._persistence_counter >= self.config.rising_persistence:
                    self._transition(DetectorState.RISING, timestamp)
                    self._start_time = timestamp
                    self._background_locked = True
                    self._persistence_counter = 0
            elif ratio < self.config.monitoring_threshold:
                self._transition(DetectorState.IDLE, timestamp)
                self._persistence_counter = 0
            else:
                self._persistence_counter = 0

        elif self._state == DetectorState.RISING:
            if flux > self._peak_flux:
                self._peak_flux = flux
                self._peak_time = timestamp
            if ratio >= self.config.active_threshold:
                self._transition(DetectorState.ACTIVE, timestamp)
            elif ratio < self.config.monitoring_threshold:
                # False alarm — return to idle
                self._reset(timestamp)

        elif self._state == DetectorState.ACTIVE:
            if flux > self._peak_flux:
                self._peak_flux = flux
                self._peak_time = timestamp
            smoothed_deriv = self.buffer.derivative(window=self.config.peak_derivative_window)
            if smoothed_deriv <= 0:
                self._transition(DetectorState.PEAK, timestamp)

        elif self._state == DetectorState.PEAK:
            drop = (self._peak_flux - flux) / self._peak_flux if self._peak_flux > 0 else 0
            if drop >= self.config.decay_drop_fraction:
                self._transition(DetectorState.DECAY, timestamp)

        elif self._state == DetectorState.DECAY:
            if ratio <= self.config.ended_threshold:
                self._transition(DetectorState.ENDED, timestamp)
                completed_event = self._finalise_event(flux, timestamp, obs_quality)

        return completed_event

    def snapshot(self) -> DetectorSnapshot:
        """Return a real-time snapshot for the frontend."""
        bg = self._background
        return DetectorSnapshot(
            detector_name="SoLEXS",
            state=self._state,
            current_flux=self.buffer.latest or 0.0,
            background_level=bg,
            threshold=bg * self.config.active_threshold,
            adaptive_threshold=bg * self.config.monitoring_threshold,
            confidence=self._compute_confidence(self.buffer.latest or 0.0, 1.0).overall,
            confidence_decomposition=self._compute_confidence(self.buffer.latest or 0.0, 1.0),
            buffer_fill=self.buffer.fill_fraction,
            observation_count=self._observation_count,
            last_event_id=self.last_event.event_id if self.last_event else None,
            events_detected=self._events_detected,
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _transition(self, new_state: DetectorState, timestamp: str) -> None:
        self._state = new_state

    def _reset(self, timestamp: str) -> None:
        self._state = DetectorState.IDLE
        self._persistence_counter = 0
        self._peak_flux = 0.0
        self._peak_time = None
        self._start_time = None
        self._background_locked = False

    def _compute_confidence(self, current_flux: float, obs_quality: float) -> ConfidenceDecomposition:
        cfg = self.config
        bg = self._background if self._background > 0 else 1.0

        peak_ratio_raw = min((self._peak_flux / bg) / 10.0, 1.0) if self._peak_flux > 0 else 0.0
        persistence_raw = min(self._observation_count / 60.0, 1.0)
        deriv_raw = min(abs(self.buffer.derivative(cfg.derivative_window)) / bg, 1.0)
        quality_raw = min(obs_quality, 1.0)

        overall = (
            cfg.confidence_weight_peak_ratio * peak_ratio_raw
            + cfg.confidence_weight_persistence * persistence_raw
            + cfg.confidence_weight_derivative * deriv_raw
            + cfg.confidence_weight_quality * quality_raw
        )
        return ConfidenceDecomposition(
            peak_ratio_score=peak_ratio_raw,
            persistence_score=persistence_raw,
            derivative_score=deriv_raw,
            quality_score=quality_raw,
            overall=min(overall, 1.0),
        )

    def _finalise_event(self, flux: float, timestamp: str, obs_quality: float) -> SolexsEvent:
        conf = self._compute_confidence(flux, obs_quality)
        thermal_rise = (self._peak_flux - self._background) / self._background if self._background > 0 else 0.0

        event = SolexsEvent(
            start_time=self._start_time,
            peak_time=self._peak_time,
            end_time=timestamp,
            peak_flux=self._peak_flux,
            background_flux=self._background,
            thermal_rise=thermal_rise,
            detection_confidence=conf.overall,
            confidence_decomposition=conf,
            quality="GOOD" if obs_quality > 0.8 else ("DEGRADED" if obs_quality > 0.5 else "POOR"),
            detector_state=DetectorState.ENDED,
            observation_count=self._observation_count,
        )
        self._events_detected += 1
        self.last_event = event
        self._reset(timestamp)
        return event
