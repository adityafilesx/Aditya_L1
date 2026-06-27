"""
HEL1OS Hard X-ray Burst Detector.

Detects impulsive hard X-ray bursts by monitoring rapid flux spikes relative
to a sigma-based adaptive background.  Uses a dedicated sliding buffer, EMA
background, and configurable sigma thresholds.

State Machine
-------------
IDLE → RISING → ACTIVE → PEAK → DECAY → ENDED

On ENDED a complete ``HeliosEvent`` is emitted with decomposed confidence.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from backend.nowcasting.buffers.sliding_buffer import SlidingBuffer
from backend.nowcasting.config import HeliosDetectorConfig, nowcast_config
from backend.nowcasting.models import (
    DetectorState,
    HeliosEvent,
    ConfidenceDecomposition,
    DetectorSnapshot,
)


class HeliosDetector:
    """HEL1OS hard X-ray impulsive burst detector with configurable parameters."""

    VERSION = "1.0.0"

    def __init__(self, config: Optional[HeliosDetectorConfig] = None):
        self.config = config or nowcast_config.helios
        self.buffer = SlidingBuffer(max_size=self.config.buffer_size)

        # State machine
        self._state = DetectorState.IDLE
        self._persistence_counter: int = 0
        self._observation_count: int = 0
        self._events_detected: int = 0

        # Adaptive background
        self._background: float = self.config.background_seed
        self._sigma: float = 0.0
        self._background_locked: bool = False

        # Peak tracking
        self._peak_flux: float = 0.0
        self._peak_time: Optional[str] = None
        self._total_energy: float = 0.0  # accumulated flux during burst

        # Timing
        self._start_time: Optional[str] = None
        self._burst_ticks: int = 0

        # Last completed event
        self.last_event: Optional[HeliosEvent] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def ingest(self, flux: float, timestamp: str, obs_quality: float = 1.0) -> Optional[HeliosEvent]:
        """Feed one observation. Returns a completed HeliosEvent on ENDED."""
        self.buffer.push(flux, timestamp)
        self._observation_count += 1

        # Update adaptive background when not locked
        if not self._background_locked:
            self._background = self.config.ema_alpha * flux + (1.0 - self.config.ema_alpha) * self._background
            self._sigma = self.buffer.std()

        sigma = self._sigma if self._sigma > 0 else 1.0
        deviation = (flux - self._background) / sigma if sigma > 0 else 0.0

        completed_event: Optional[HeliosEvent] = None

        # --- State machine ---
        if self._state == DetectorState.IDLE:
            if deviation >= self.config.spike_sigma:
                self._persistence_counter += 1
                if self._persistence_counter >= 1:
                    self._transition(DetectorState.RISING, timestamp)
                    self._start_time = timestamp
                    self._background_locked = True
                    self._burst_ticks = 0
                    self._total_energy = 0.0
                    self._peak_flux = flux
                    self._peak_time = timestamp
                    self._persistence_counter = 0
            else:
                self._persistence_counter = 0

        elif self._state == DetectorState.RISING:
            self._burst_ticks += 1
            self._total_energy += flux
            if flux > self._peak_flux:
                self._peak_flux = flux
                self._peak_time = timestamp
            if deviation >= self.config.spike_sigma:
                self._persistence_counter += 1
                if self._persistence_counter >= self.config.rising_persistence:
                    self._transition(DetectorState.ACTIVE, timestamp)
                    self._persistence_counter = 0
            else:
                # Spike did not persist — false alarm
                self._reset(timestamp)

        elif self._state == DetectorState.ACTIVE:
            self._burst_ticks += 1
            self._total_energy += flux
            if flux > self._peak_flux:
                self._peak_flux = flux
                self._peak_time = timestamp
            # Check for peak (next sample drops)
            if flux < self._peak_flux:
                self._transition(DetectorState.PEAK, timestamp)
            # Auto-close if burst exceeds maximum duration
            if self._burst_ticks >= self.config.max_burst_duration_s:
                self._transition(DetectorState.PEAK, timestamp)

        elif self._state == DetectorState.PEAK:
            self._burst_ticks += 1
            self._total_energy += flux
            peak_drop = (self._peak_flux - flux) / sigma if sigma > 0 else 0
            if peak_drop >= self.config.decay_sigma:
                self._transition(DetectorState.DECAY, timestamp)

        elif self._state == DetectorState.DECAY:
            self._burst_ticks += 1
            self._total_energy += flux
            if deviation <= self.config.ended_sigma:
                self._transition(DetectorState.ENDED, timestamp)
                completed_event = self._finalise_event(flux, timestamp, obs_quality)

        return completed_event

    def snapshot(self) -> DetectorSnapshot:
        """Return a real-time snapshot for the frontend."""
        sigma = self._sigma if self._sigma > 0 else 1.0
        return DetectorSnapshot(
            detector_name="HEL1OS",
            state=self._state,
            current_flux=self.buffer.latest or 0.0,
            background_level=self._background,
            threshold=self._background + self.config.spike_sigma * sigma,
            adaptive_threshold=self._background + self.config.ended_sigma * sigma,
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
        self._burst_ticks = 0
        self._total_energy = 0.0
        self._background_locked = False

    def _compute_confidence(self, current_flux: float, obs_quality: float) -> ConfidenceDecomposition:
        cfg = self.config
        sigma = self._sigma if self._sigma > 0 else 1.0
        bg = self._background if self._background > 0 else 1.0

        sigma_score = min(abs(current_flux - bg) / (sigma * 10.0), 1.0) if self._peak_flux > 0 else 0.0
        duration_score = min(self._burst_ticks / 30.0, 1.0)
        energy_score = min(self._total_energy / (bg * 100.0), 1.0)
        quality_raw = min(obs_quality, 1.0)

        overall = (
            cfg.confidence_weight_sigma * sigma_score
            + cfg.confidence_weight_duration * duration_score
            + cfg.confidence_weight_energy * energy_score
            + cfg.confidence_weight_quality * quality_raw
        )
        return ConfidenceDecomposition(
            peak_ratio_score=sigma_score,
            persistence_score=duration_score,
            derivative_score=energy_score,
            quality_score=quality_raw,
            overall=min(overall, 1.0),
        )

    def _finalise_event(self, flux: float, timestamp: str, obs_quality: float) -> HeliosEvent:
        conf = self._compute_confidence(flux, obs_quality)
        event = HeliosEvent(
            start_time=self._start_time,
            peak_time=self._peak_time,
            end_time=timestamp,
            peak_energy=self._peak_flux,
            peak_counts=self._total_energy,
            burst_duration_s=float(self._burst_ticks),
            detection_confidence=conf.overall,
            confidence_decomposition=conf,
            detector_state=DetectorState.ENDED,
            observation_count=self._observation_count,
        )
        self._events_detected += 1
        self.last_event = event
        self._reset(timestamp)
        return event
