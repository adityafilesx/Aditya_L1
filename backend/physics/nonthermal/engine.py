"""
Non-Thermal Characterization Engine.

Characterizes the impulsive, non-thermal component of a solar flare from
the hard X-ray (HEL1OS) flux profile:
  - Peak electron energy
  - Burst energy (integrated HEL1OS flux)
  - Acceleration duration
  - Impulsive phase duration
  - Energy distribution over time
"""

from __future__ import annotations

import math
from typing import List, Tuple

from backend.physics.models import NonThermalProfile, ThermalQuality, ComputationStatus
from backend.nowcasting.models import MasterFlareEntry


class NonThermalEngine:
    """Computes the non-thermal profile from HEL1OS burst data."""

    VERSION = "1.0.0"

    def characterize(
        self,
        entry: MasterFlareEntry,
        helios_history: List[float],
    ) -> Tuple[NonThermalProfile, ThermalQuality]:
        """Characterize non-thermal properties from HEL1OS flux history."""

        sample_count = len(helios_history)

        if sample_count < 3:
            return (
                NonThermalProfile(),
                ThermalQuality(
                    sample_count=sample_count,
                    computation_status=ComputationStatus.INSUFFICIENT,
                    limiting_factor="No HEL1OS burst data available",
                ),
            )

        # Background estimation from first 10% of samples
        bg_window = max(3, sample_count // 10)
        background = sum(helios_history[:bg_window]) / bg_window
        background = max(background, 0.1)

        # Find burst region (above 2× background)
        burst_threshold = background * 2.0
        burst_indices = [i for i, v in enumerate(helios_history) if v > burst_threshold]

        if not burst_indices:
            return (
                NonThermalProfile(background_level=background),
                ThermalQuality(
                    sample_count=sample_count,
                    data_coverage=min(sample_count / 30.0, 1.0),
                    computation_status=ComputationStatus.DEGRADED,
                    limiting_factor="No significant burst detected in HEL1OS data",
                ),
            )

        burst_start = burst_indices[0]
        burst_end = burst_indices[-1]
        impulsive_phase_duration = float(burst_end - burst_start + 1)

        # Peak within burst
        burst_fluxes = helios_history[burst_start:burst_end + 1]
        peak_counts = max(burst_fluxes)

        # Peak electron energy (proxy: scale peak counts)
        peak_electron_energy = 10.0 + 50.0 * math.tanh(peak_counts / (background * 10.0))

        # Burst energy = integrated flux above background
        burst_energy = sum(f - background for f in burst_fluxes if f > background)

        # Hard X-ray energy (erg) — simplified conversion
        hard_xray_energy = burst_energy * 1e-3 * 1.6e-9  # rough keV→erg

        # Electron flux
        electron_flux = peak_counts / max(impulsive_phase_duration, 1.0)

        # Acceleration duration (time from burst start to peak)
        peak_idx = burst_fluxes.index(peak_counts)
        acceleration_duration = float(peak_idx + 1)

        # Energy distribution (normalised burst profile)
        max_bf = max(burst_fluxes) if max(burst_fluxes) > 0 else 1.0
        energy_distribution = [round(f / max_bf, 4) for f in burst_fluxes]

        # Quality
        data_coverage = min(sample_count / 30.0, 1.0)
        status = ComputationStatus.GOOD
        limiting = ""
        if impulsive_phase_duration < 3:
            status = ComputationStatus.DEGRADED
            limiting = "Very short burst duration"

        profile = NonThermalProfile(
            peak_electron_energy=round(peak_electron_energy, 3),
            burst_energy=round(burst_energy, 3),
            hard_xray_energy=hard_xray_energy,
            electron_flux=round(electron_flux, 4),
            acceleration_duration=round(acceleration_duration, 2),
            energy_distribution=energy_distribution[-30:],
            impulsive_phase_duration=round(impulsive_phase_duration, 2),
        )

        quality = ThermalQuality(
            data_coverage=round(data_coverage, 3),
            sample_count=sample_count,
            computation_status=status,
            limiting_factor=limiting,
        )

        return profile, quality
