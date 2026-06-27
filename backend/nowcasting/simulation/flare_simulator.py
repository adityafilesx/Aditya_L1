"""
Dedicated flare profile simulator.

Generates realistic solar flare light-curve profiles that are injected into
the raw telemetry stream. Completely separate from the real telemetry generator
so that simulation parameters can be tuned independently.

The simulator models:
  - Quiet-Sun baseline with Gaussian noise
  - Gradual thermal rise for SoLEXS (soft X-ray)
  - Impulsive burst for HEL1OS (hard X-ray) preceding the thermal peak
    (Neupert Effect)
  - Configurable duration, peak intensity, and noise levels
"""

from __future__ import annotations

import math
import random
from datetime import datetime, timezone
from typing import Tuple, Optional

from backend.nowcasting.config import SimulationConfig, nowcast_config


class FlareProfile:
    """In-progress simulated flare with deterministic time-series shape."""

    def __init__(self, config: SimulationConfig):
        self.duration = random.randint(config.flare_min_duration_s, config.flare_max_duration_s)
        self.peak_multiplier = random.uniform(config.flare_peak_multiplier_min, config.flare_peak_multiplier_max)
        self.rise_fraction = random.uniform(0.25, 0.40)  # fraction of duration spent rising
        self.peak_time_fraction = self.rise_fraction
        self.decay_fraction = 1.0 - self.rise_fraction
        self.tick = 0

        # HEL1OS burst parameters
        self.helios_spike_start = max(0, int(self.peak_time_fraction * self.duration) - config.helios_spike_delay_s - 2)
        self.helios_burst_duration = max(3, int(self.duration * config.helios_burst_fraction))

    @property
    def is_active(self) -> bool:
        return self.tick < self.duration

    def advance(self) -> Tuple[float, float]:
        """Advance one tick and return (solexs_multiplier, helios_multiplier).

        Multipliers are applied on top of the quiet-Sun baseline.
        """
        if self.tick >= self.duration:
            return 1.0, 1.0

        t = self.tick / self.duration  # normalised time 0–1
        self.tick += 1

        # --- SoLEXS: gradual thermal rise & decay ---
        if t < self.rise_fraction:
            # Smooth rise using half-cosine
            phase = t / self.rise_fraction
            solexs_mult = 1.0 + (self.peak_multiplier - 1.0) * (0.5 - 0.5 * math.cos(math.pi * phase))
        else:
            # Exponential decay
            decay_phase = (t - self.rise_fraction) / self.decay_fraction
            solexs_mult = 1.0 + (self.peak_multiplier - 1.0) * math.exp(-3.0 * decay_phase)

        # --- HEL1OS: impulsive burst ---
        helios_mult = 1.0
        burst_start_t = self.helios_spike_start / self.duration
        burst_end_t = (self.helios_spike_start + self.helios_burst_duration) / self.duration
        if burst_start_t <= t <= burst_end_t:
            burst_phase = (t - burst_start_t) / (burst_end_t - burst_start_t)
            # Sharp Gaussian-like pulse
            helios_mult = 1.0 + (self.peak_multiplier * 1.5 - 1.0) * math.exp(-8.0 * (burst_phase - 0.3) ** 2)

        return solexs_mult, helios_mult


class FlareSimulator:
    """Manages flare injection into the telemetry stream.

    Call ``generate()`` once per second (at the observation cadence) to get
    the current (solexs_flux, helios_flux) values.  The simulator
    autonomously decides when to inject a new flare based on the configured
    probability.
    """

    def __init__(self, config: Optional[SimulationConfig] = None):
        self.config = config or nowcast_config.simulation
        self._active_flare: Optional[FlareProfile] = None
        self._tick_count: int = 0

    @property
    def is_flaring(self) -> bool:
        return self._active_flare is not None and self._active_flare.is_active

    def generate(self) -> Tuple[float, float]:
        """Generate one tick of (solexs_flux, helios_flux)."""
        self._tick_count += 1

        solexs_base = self.config.solexs_quiet_flux
        helios_base = self.config.helios_quiet_flux

        # Possibly start a new flare
        if not self.is_flaring and random.random() < self.config.flare_probability_per_tick:
            self._active_flare = FlareProfile(self.config)

        # Compute multipliers
        sol_mult, hel_mult = 1.0, 1.0
        if self.is_flaring:
            sol_mult, hel_mult = self._active_flare.advance()  # type: ignore[union-attr]
            if not self._active_flare.is_active:  # type: ignore[union-attr]
                self._active_flare = None

        # Apply noise
        noise_sol = random.gauss(0, solexs_base * self.config.noise_std_fraction)
        noise_hel = random.gauss(0, helios_base * self.config.noise_std_fraction)

        solexs_flux = max(0.1, solexs_base * sol_mult + noise_sol)
        helios_flux = max(0.1, helios_base * hel_mult + noise_hel)

        return solexs_flux, helios_flux


# Global singleton
flare_simulator = FlareSimulator()
