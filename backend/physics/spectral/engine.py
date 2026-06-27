"""
Spectral Analysis Engine.

Decomposes the flare emission into thermal and non-thermal components and
estimates the power-law index of the hard X-ray spectrum.
"""

from __future__ import annotations

import math
from typing import List, Tuple

from backend.physics.models import SpectralProfile, SpectralQuality, ComputationStatus
from backend.nowcasting.models import MasterFlareEntry


class SpectralEngine:
    """Spectral decomposition engine."""

    VERSION = "1.0.0"

    def characterize(
        self,
        entry: MasterFlareEntry,
        solexs_history: List[float],
        helios_history: List[float],
    ) -> Tuple[SpectralProfile, SpectralQuality]:

        sol_n = len(solexs_history)
        hel_n = len(helios_history)

        if sol_n < 3 or hel_n < 3:
            return (
                SpectralProfile(),
                SpectralQuality(
                    computation_status=ComputationStatus.INSUFFICIENT,
                    limiting_factor="Insufficient dual-instrument data",
                ),
            )

        # Thermal / non-thermal decomposition by energy ratio
        sol_peak = max(solexs_history)
        hel_peak = max(helios_history)
        total = sol_peak + hel_peak
        thermal_frac = sol_peak / max(total, 0.1)
        nonthermal_frac = hel_peak / max(total, 0.1)

        # Power-law index from log-log slope of HEL1OS burst
        # Simulate: steeper spectrum → larger γ → more thermal-dominated
        bg_hel = sum(helios_history[:max(3, hel_n // 10)]) / max(3, hel_n // 10)
        bg_hel = max(bg_hel, 0.1)
        ratios = [f / bg_hel for f in helios_history if f > bg_hel * 1.5]
        if len(ratios) >= 2:
            # Log-ratio slope approximation
            log_ratios = [math.log10(max(r, 0.01)) for r in ratios]
            n = len(log_ratios)
            x = list(range(n))
            x_mean = sum(x) / n
            y_mean = sum(log_ratios) / n
            num = sum((x[i] - x_mean) * (log_ratios[i] - y_mean) for i in range(n))
            den = sum((x[i] - x_mean) ** 2 for i in range(n))
            slope = num / max(abs(den), 1e-6)
            power_law_index = max(1.5, min(8.0, 4.0 - slope * 5.0))
        else:
            power_law_index = 4.0  # default

        # Energy cutoffs
        low_energy_cutoff = 1.0 + 5.0 * thermal_frac
        high_energy_cutoff = 50.0 + 100.0 * nonthermal_frac

        # Goodness of fit (simulated)
        residual = abs(thermal_frac + nonthermal_frac - 1.0)
        gof = max(0.0, 1.0 - residual * 10.0)

        # Quality
        spectral_coverage = min(1.0, (sol_n + hel_n) / 60.0)
        status = ComputationStatus.GOOD
        limiting = ""
        if sol_n < 10 or hel_n < 10:
            status = ComputationStatus.DEGRADED
            limiting = "Limited spectral coverage"

        profile = SpectralProfile(
            thermal_component=round(thermal_frac, 4),
            nonthermal_component=round(nonthermal_frac, 4),
            spectral_residual=round(residual, 6),
            power_law_index=round(power_law_index, 3),
            low_energy_cutoff=round(low_energy_cutoff, 2),
            high_energy_cutoff=round(high_energy_cutoff, 2),
            goodness_of_fit=round(gof, 4),
        )

        quality = SpectralQuality(
            fit_residual_norm=round(residual, 6),
            spectral_coverage=round(spectral_coverage, 3),
            computation_status=status,
            limiting_factor=limiting,
        )

        return profile, quality
