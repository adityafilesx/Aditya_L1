"""
Temporal Characterization Engine.

Computes temporal metrics for the flare (rise time, decay time, duration,
integrated flux, signal-to-noise ratio) from the catalog entry and flux buffers.
"""

from __future__ import annotations

import math
from datetime import datetime
from typing import List, Tuple, Optional

from backend.physics.models import EventCharacterization, CharacterizationQuality, ComputationStatus
from backend.nowcasting.models import MasterFlareEntry


def _parse_ts(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


class CharacterizationEngine:
    """Computes basic temporal characterization metrics."""

    VERSION = "1.0.0"

    def characterize(
        self,
        entry: MasterFlareEntry,
        solexs_history: List[float],
    ) -> Tuple[EventCharacterization, CharacterizationQuality]:

        start_dt = _parse_ts(entry.unified_start)
        peak_dt = _parse_ts(entry.unified_peak)
        end_dt = _parse_ts(entry.unified_end)

        rise_time = 0.0
        decay_time = 0.0
        duration = 0.0

        if start_dt and end_dt:
            duration = (end_dt - start_dt).total_seconds()
        
        if start_dt and peak_dt:
            rise_time = (peak_dt - start_dt).total_seconds()
            
        if peak_dt and end_dt:
            decay_time = (end_dt - peak_dt).total_seconds()

        # Integrated flux (simplified approximation from history)
        bg = min(solexs_history[:10]) if len(solexs_history) >= 10 else 30.0
        net_history = [max(0, f - bg) for f in solexs_history]
        integrated_flux = sum(net_history)

        # SNR (Peak to Background ratio)
        snr = entry.peak_flux / max(bg, 1.0) if entry.peak_flux > 0 else 0.0

        # Maximum derivative
        max_deriv = 0.0
        if len(solexs_history) > 2:
            derivs = [solexs_history[i] - solexs_history[i-1] for i in range(1, len(solexs_history))]
            max_deriv = max(derivs)

        profile = EventCharacterization(
            start_time=entry.unified_start,
            peak_time=entry.unified_peak,
            end_time=entry.unified_end,
            rise_time=round(max(0, rise_time), 1),
            decay_time=round(max(0, decay_time), 1),
            duration=round(max(0, duration), 1),
            integrated_flux=round(integrated_flux, 1),
            peak_flux=entry.peak_flux,
            peak_hard_xray=entry.peak_energy,
            peak_soft_xray=entry.peak_flux,
            maximum_derivative=round(max_deriv, 2),
            background_level=round(bg, 2),
            signal_to_noise_ratio=round(snr, 2),
        )

        # Quality
        status = ComputationStatus.GOOD
        limiting = ""
        if duration <= 0:
            status = ComputationStatus.DEGRADED
            limiting = "Invalid temporal bounds"
        
        quality = CharacterizationQuality(
            timing_precision=1.0 if duration > 0 else 0.0,
            snr_adequacy=min(1.0, snr / 10.0),
            computation_status=status,
            limiting_factor=limiting,
        )

        return profile, quality
