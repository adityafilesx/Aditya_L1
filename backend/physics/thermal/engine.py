"""
Thermal Characterization Engine.

Computes thermal properties of a solar flare from the soft X-ray (SoLEXS)
flux profile:
  - Peak temperature (from soft/hard X-ray ratio via Wien approximation)
  - Emission measure (from flux and temperature)
  - Heating / cooling rates (temporal derivatives of temperature)
  - Thermal energy (simplified: 3 k_B T sqrt(EM) V)
  - Temperature gradient
"""

from __future__ import annotations

import math
from typing import List, Tuple

from backend.physics.models import (
    ThermalProfile,
    ThermalQuality,
    ComputationStatus,
)
from backend.nowcasting.models import MasterFlareEntry


# Physical constants (CGS)
K_B = 1.38e-16       # Boltzmann constant (erg/K)
MK_TO_K = 1.0e6      # mega-Kelvin to Kelvin
LOOP_VOLUME = 1e27    # cm³ — representative coronal loop volume


class ThermalEngine:
    """Computes the thermal profile for a detected flare."""

    VERSION = "1.0.0"

    def characterize(
        self,
        entry: MasterFlareEntry,
        solexs_history: List[float],
        helios_history: List[float],
    ) -> Tuple[ThermalProfile, ThermalQuality]:
        """Characterize thermal properties from flux histories."""

        sample_count = len(solexs_history)

        # Quality gate
        if sample_count < 5:
            return (
                ThermalProfile(),
                ThermalQuality(
                    sample_count=sample_count,
                    computation_status=ComputationStatus.INSUFFICIENT,
                    limiting_factor="Insufficient SoLEXS samples",
                ),
            )

        # --- Temperature estimation ---
        # Use ratio of soft/hard X-ray as proxy for temperature
        # Higher ratio → higher temperature (thermal-dominated emission)
        peak_sol = entry.peak_flux if entry.peak_flux > 0 else max(solexs_history)
        peak_hel = entry.peak_energy if entry.peak_energy > 0 else (max(helios_history) if helios_history else 1.0)
        ratio = peak_sol / max(peak_hel, 0.1)

        # Map ratio to temperature (MK): T ~ 5 + 15 * tanh(ratio/5)
        peak_temp_mk = 5.0 + 15.0 * math.tanh(ratio / 5.0)

        # --- Temperature evolution ---
        bg = min(solexs_history[:10]) if len(solexs_history) >= 10 else min(solexs_history)
        bg = max(bg, 0.1)
        temp_evolution = []
        for flux in solexs_history:
            r = flux / bg
            t = 5.0 + 15.0 * math.tanh(r / 5.0)
            temp_evolution.append(round(t, 3))

        # --- Heating and cooling rates ---
        heating_rate = 0.0
        cooling_rate = 0.0
        if len(temp_evolution) >= 3:
            derivatives = [temp_evolution[i + 1] - temp_evolution[i] for i in range(len(temp_evolution) - 1)]
            positive_derivs = [d for d in derivatives if d > 0]
            negative_derivs = [d for d in derivatives if d < 0]
            heating_rate = sum(positive_derivs) / max(len(positive_derivs), 1)
            cooling_rate = abs(sum(negative_derivs) / max(len(negative_derivs), 1))

        # --- Temperature gradient ---
        temp_gradient = 0.0
        if len(temp_evolution) >= 2:
            temp_gradient = temp_evolution[-1] - temp_evolution[0]

        # --- Emission measure (log-scale) ---
        # EM ~ flux / T^2 (simplified from optically thin plasma)
        em_raw = peak_sol / max(peak_temp_mk ** 2, 1.0)
        emission_measure = 48.0 + math.log10(max(em_raw, 1e-10))

        # --- Thermal energy ---
        # E_th = 3 k_B T sqrt(EM) V (very simplified)
        thermal_energy = 3.0 * K_B * (peak_temp_mk * MK_TO_K) * math.sqrt(max(10 ** emission_measure, 1e40)) * LOOP_VOLUME ** 0.5

        # --- Quality ---
        data_coverage = min(sample_count / 60.0, 1.0)
        status = ComputationStatus.GOOD
        limiting = ""
        if sample_count < 10:
            status = ComputationStatus.INSUFFICIENT
            limiting = "Very few SoLEXS samples"
        elif sample_count < 30:
            status = ComputationStatus.DEGRADED
            limiting = "Limited SoLEXS history"

        profile = ThermalProfile(
            peak_temperature=round(peak_temp_mk, 3),
            temperature_evolution=temp_evolution[-60:],  # last 60 samples
            emission_measure=round(emission_measure, 3),
            heating_rate=round(heating_rate, 4),
            cooling_rate=round(cooling_rate, 4),
            thermal_energy=thermal_energy,
            temperature_gradient=round(temp_gradient, 4),
        )

        quality = ThermalQuality(
            data_coverage=round(data_coverage, 3),
            sample_count=sample_count,
            computation_status=status,
            limiting_factor=limiting,
        )

        return profile, quality
