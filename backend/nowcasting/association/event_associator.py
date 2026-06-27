"""
Temporal Event Association Engine.

Determines whether a HEL1OS impulsive event is physically related to a
SoLEXS thermal event by evaluating:

  1. Temporal overlap of the two event intervals
  2. Neupert timing — HEL1OS hard X-ray peak should precede the SoLEXS
     soft X-ray peak (the Neupert Effect)
  3. Flux-profile correlation (placeholder — uses peak ratio for now)

Outputs an ``EventAssociation`` with decomposed confidence and a tri-state
classification: ASSOCIATED / AMBIGUOUS / NOT_ASSOCIATED.
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional

from backend.nowcasting.config import AssociationConfig, nowcast_config
from backend.nowcasting.models import (
    SolexsEvent,
    HeliosEvent,
    EventAssociation,
    AssociationStatus,
)


def _parse_ts(ts: Optional[str]) -> Optional[datetime]:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except Exception:
        return None


class EventAssociator:
    """Associates SoLEXS and HEL1OS events via temporal analysis."""

    VERSION = "1.0.0"

    def __init__(self, config: Optional[AssociationConfig] = None):
        self.config = config or nowcast_config.association

    def associate(self, sol_event: SolexsEvent, hel_event: HeliosEvent) -> EventAssociation:
        """Evaluate whether two events belong to the same physical flare."""

        sol_start = _parse_ts(sol_event.start_time)
        sol_end = _parse_ts(sol_event.end_time)
        sol_peak = _parse_ts(sol_event.peak_time)
        hel_start = _parse_ts(hel_event.start_time)
        hel_end = _parse_ts(hel_event.end_time)
        hel_peak = _parse_ts(hel_event.peak_time)

        # ----- 1. Temporal overlap -----
        overlap_s = 0.0
        if sol_start and sol_end and hel_start and hel_end:
            overlap_start = max(sol_start, hel_start)
            overlap_end = min(sol_end, hel_end)
            overlap_s = max(0.0, (overlap_end - overlap_start).total_seconds())

        total_span = 0.0
        if sol_start and sol_end and hel_start and hel_end:
            span_start = min(sol_start, hel_start)
            span_end = max(sol_end, hel_end)
            total_span = max(1.0, (span_end - span_start).total_seconds())

        temporal_overlap_score = min(overlap_s / total_span, 1.0) if total_span > 0 else 0.0

        # ----- 2. Neupert timing -----
        neupert_score = 0.0
        if hel_peak and sol_peak:
            delay = (sol_peak - hel_peak).total_seconds()
            if 0 <= delay <= self.config.neupert_max_delay_s:
                # Perfect Neupert: HEL1OS peaks before SoLEXS
                neupert_score = 1.0 - (delay / self.config.neupert_max_delay_s)
            elif delay < 0 and abs(delay) < self.config.neupert_max_delay_s:
                # Reversed timing — partial credit
                neupert_score = 0.3 * (1.0 - abs(delay) / self.config.neupert_max_delay_s)

        # ----- 3. Flux correlation (simplified) -----
        flux_corr = 0.0
        if sol_event.peak_flux > 0 and hel_event.peak_energy > 0:
            # Both instruments detected significant activity
            flux_corr = min(1.0, 0.5 + 0.5 * min(sol_event.peak_flux, hel_event.peak_energy) / max(sol_event.peak_flux, hel_event.peak_energy))

        # ----- Weighted confidence -----
        confidence = (
            self.config.weight_temporal_overlap * temporal_overlap_score
            + self.config.weight_neupert_timing * neupert_score
            + self.config.weight_flux_correlation * flux_corr
        )
        confidence = min(confidence, 1.0)

        # ----- Classification -----
        if confidence >= self.config.association_threshold:
            status = AssociationStatus.ASSOCIATED
        elif confidence >= self.config.ambiguous_threshold:
            status = AssociationStatus.AMBIGUOUS
        else:
            status = AssociationStatus.NOT_ASSOCIATED

        return EventAssociation(
            solexs_event_id=sol_event.event_id,
            helios_event_id=hel_event.event_id,
            temporal_overlap_s=overlap_s,
            neupert_timing_score=neupert_score,
            flux_correlation=flux_corr,
            association_confidence=confidence,
            status=status,
        )
