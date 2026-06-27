"""
Neupert Effect Analysis Engine.

Evaluates whether the flare follows the Neupert effect, which states that the
soft X-ray flux is approximately proportional to the time integral of the
hard X-ray flux (or equivalently, the hard X-ray flux is proportional to the
time derivative of the soft X-ray flux).
"""

from __future__ import annotations

import math
from typing import List, Tuple

from backend.physics.models import NeupertProfile, NeupertQuality, ComputationStatus, NeupertClassification
from backend.nowcasting.models import MasterFlareEntry


class NeupertEngine:
    """Analyzes the Neupert effect relationship between SoLEXS and HEL1OS."""

    VERSION = "1.0.0"

    def characterize(
        self,
        entry: MasterFlareEntry,
        solexs_history: List[float],
        helios_history: List[float],
    ) -> Tuple[NeupertProfile, NeupertQuality]:

        sol_n = len(solexs_history)
        hel_n = len(helios_history)

        if sol_n < 10 or hel_n < 10 or not entry.solexs_event or not entry.helios_event:
            return (
                NeupertProfile(),
                NeupertQuality(
                    computation_status=ComputationStatus.INSUFFICIENT,
                    limiting_factor="Insufficient dual-instrument data or missing associated events",
                ),
            )

        # 1. Temporal offset (HEL1OS peak should precede SoLEXS peak)
        sol_peak_time = entry.solexs_event.peak_time
        hel_peak_time = entry.helios_event.peak_time

        neupert_offset = 0.0
        if sol_peak_time and hel_peak_time:
            # Parse ISO 8601 strings
            try:
                from datetime import datetime
                sol_dt = datetime.fromisoformat(sol_peak_time.replace("Z", "+00:00"))
                hel_dt = datetime.fromisoformat(hel_peak_time.replace("Z", "+00:00"))
                neupert_offset = (sol_dt - hel_dt).total_seconds()
            except Exception:
                pass

        # 2. Correlation between cumulative HXR and SXR
        # For a perfect Neupert effect, integral(HXR) ~ SXR
        # We simulate this by comparing the normalized integral of HEL1OS to normalized SoLEXS
        
        # We need overlapping temporal windows. For simplicity in this demo, 
        # we assume the histories end at the same time and just align the tails.
        overlap_len = min(sol_n, hel_n)
        s_hist = solexs_history[-overlap_len:]
        h_hist = helios_history[-overlap_len:]

        # Background subtraction
        s_bg = min(s_hist[:max(3, overlap_len // 10)])
        h_bg = min(h_hist[:max(3, overlap_len // 10)])

        s_net = [max(0.0, s - s_bg) for s in s_hist]
        h_net = [max(0.0, h - h_bg) for h in h_hist]

        # Cumulative integral of HXR
        h_integral = []
        current_sum = 0.0
        for h in h_net:
            current_sum += h
            h_integral.append(current_sum)

        # Normalize both to 0-1
        max_s = max(s_net) if max(s_net) > 0 else 1.0
        max_h_int = max(h_integral) if max(h_integral) > 0 else 1.0

        s_norm = [s / max_s for s in s_net]
        h_int_norm = [h / max_h_int for h in h_integral]

        # Pearson correlation
        n = overlap_len
        sum_x = sum(h_int_norm)
        sum_y = sum(s_norm)
        sum_x2 = sum(x*x for x in h_int_norm)
        sum_y2 = sum(y*y for y in s_norm)
        sum_xy = sum(x*y for x, y in zip(h_int_norm, s_norm))

        denominator = math.sqrt(max(0, (n * sum_x2 - sum_x**2) * (n * sum_y2 - sum_y**2)))
        correlation = (n * sum_xy - sum_x * sum_y) / denominator if denominator > 0 else 0.0

        neupert_score = max(0.0, correlation)

        # 3. Consistency and Classification
        neupert_consistency = 0.0
        classification = NeupertClassification.UNDETERMINED

        if neupert_offset > 0 and neupert_score > 0.8:
            classification = NeupertClassification.CONSISTENT
            neupert_consistency = neupert_score
        elif neupert_offset >= 0 and neupert_score > 0.5:
            classification = NeupertClassification.PARTIAL
            neupert_consistency = neupert_score * 0.8
        else:
            classification = NeupertClassification.ANOMALOUS
            neupert_consistency = max(0.0, neupert_score * 0.5)

        neupert_confidence = min(1.0, overlap_len / 60.0)

        # Quality
        status = ComputationStatus.GOOD
        limiting = ""
        if overlap_len < 30:
            status = ComputationStatus.DEGRADED
            limiting = "Short overlap window"

        profile = NeupertProfile(
            neupert_offset=round(neupert_offset, 2),
            neupert_score=round(neupert_score, 4),
            neupert_consistency=round(neupert_consistency, 4),
            neupert_confidence=round(neupert_confidence, 4),
            neupert_classification=classification,
            neupert_timeline=[round(v, 4) for v in h_int_norm[-60:]], # last 60 normalized integral values
        )

        quality = NeupertQuality(
            correlation_validity=round(neupert_confidence, 3),
            temporal_coverage=round(overlap_len / 120.0, 3),
            computation_status=status,
            limiting_factor=limiting,
        )

        return profile, quality
