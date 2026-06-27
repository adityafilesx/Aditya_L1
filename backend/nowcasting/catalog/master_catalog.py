"""
Unified Master Flare Catalog.

The single source of truth for all detected solar flares across the platform.
Every entry carries full provenance and is version-tracked so that downstream
consumers (forecasting, decision support, reporting) always reference a
consistent, auditable record.

Supports: add, update, query active/history/by-id, search, statistics, export.
"""

from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict
import json

from backend.nowcasting.config import nowcast_config
from backend.nowcasting.models import (
    SolexsEvent,
    HeliosEvent,
    EventAssociation,
    MasterFlareEntry,
    CatalogProvenance,
    DetectorState,
    FlarePhase,
    EventLifecycle,
    PhaseTransition,
)


class MasterCatalog:
    """In-memory Unified Master Flare Catalog with provenance & versioning."""

    def __init__(self):
        self._entries: List[MasterFlareEntry] = []
        self._counter: int = 0

    # ------------------------------------------------------------------
    # Mutations
    # ------------------------------------------------------------------

    def create_entry(
        self,
        solexs_event: Optional[SolexsEvent] = None,
        helios_event: Optional[HeliosEvent] = None,
        association: Optional[EventAssociation] = None,
    ) -> MasterFlareEntry:
        """Create a new catalog entry from detected events."""

        self._counter += 1
        now = datetime.utcnow()
        master_id = f"MFC-{now.strftime('%Y%m%d')}-{self._counter:03d}"

        # Unified timing
        times = []
        if solexs_event and solexs_event.start_time:
            times.append(solexs_event.start_time)
        if helios_event and helios_event.start_time:
            times.append(helios_event.start_time)
        unified_start = min(times) if times else now.isoformat() + "Z"

        peak_times = []
        if solexs_event and solexs_event.peak_time:
            peak_times.append(solexs_event.peak_time)
        if helios_event and helios_event.peak_time:
            peak_times.append(helios_event.peak_time)
        unified_peak = max(peak_times) if peak_times else None

        end_times = []
        if solexs_event and solexs_event.end_time:
            end_times.append(solexs_event.end_time)
        if helios_event and helios_event.end_time:
            end_times.append(helios_event.end_time)
        unified_end = max(end_times) if end_times else None

        # Confidence
        confidences = []
        if solexs_event:
            confidences.append(solexs_event.detection_confidence)
        if helios_event:
            confidences.append(helios_event.detection_confidence)
        if association:
            confidences.append(association.association_confidence)
        avg_conf = sum(confidences) / len(confidences) if confidences else 0.0

        # Quality
        quality = "GOOD"
        if solexs_event and solexs_event.quality == "POOR":
            quality = "POOR"
        elif solexs_event and solexs_event.quality == "DEGRADED":
            quality = "DEGRADED"

        # Lifecycle
        lifecycle = EventLifecycle(
            current_phase=FlarePhase.DETECTED,
            transitions=[
                PhaseTransition(
                    from_phase=FlarePhase.WAITING,
                    to_phase=FlarePhase.DETECTED,
                    timestamp=now.isoformat() + "Z",
                    reason="Initial detection",
                )
            ],
            started_at=unified_start,
        )

        # Provenance
        provenance = CatalogProvenance(
            created_at=now.isoformat() + "Z",
            last_updated_at=now.isoformat() + "Z",
            catalog_version=nowcast_config.catalog_version,
            pipeline_version=nowcast_config.pipeline_version,
            solexs_detector_version="1.0.0",
            helios_detector_version="1.0.0",
            association_engine_version="1.0.0",
            update_count=0,
            change_log=["Entry created"],
        )

        entry = MasterFlareEntry(
            master_id=master_id,
            solexs_event=solexs_event,
            helios_event=helios_event,
            association=association,
            unified_start=unified_start,
            unified_peak=unified_peak,
            unified_end=unified_end,
            peak_flux=solexs_event.peak_flux if solexs_event else 0.0,
            peak_energy=helios_event.peak_energy if helios_event else 0.0,
            quality=quality,
            confidence=avg_conf,
            current_state=DetectorState.ENDED,
            phase=FlarePhase.DETECTED,
            lifecycle=lifecycle,
            provenance=provenance,
        )
        self._entries.append(entry)
        return entry

    def update_phase(self, master_id: str, phase: FlarePhase, reason: str = "") -> Optional[MasterFlareEntry]:
        """Transition a catalog entry to a new phase."""
        entry = self.get_by_id(master_id)
        if not entry:
            return None
        now = datetime.utcnow().isoformat() + "Z"
        entry.lifecycle.transitions.append(
            PhaseTransition(
                from_phase=entry.phase,
                to_phase=phase,
                timestamp=now,
                reason=reason,
            )
        )
        entry.phase = phase
        entry.lifecycle.current_phase = phase
        if phase in (FlarePhase.COMPLETED, FlarePhase.ARCHIVED):
            entry.lifecycle.completed_at = now
        entry.provenance.last_updated_at = now
        entry.provenance.update_count += 1
        entry.provenance.change_log.append(f"Phase → {phase.value}: {reason}")
        return entry

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_active(self) -> List[MasterFlareEntry]:
        active_phases = {FlarePhase.DETECTED, FlarePhase.CONFIRMED, FlarePhase.ASSOCIATED, FlarePhase.ACTIVE, FlarePhase.PEAK, FlarePhase.DECAY}
        return [e for e in self._entries if e.phase in active_phases]

    def get_history(self, limit: int = 50) -> List[MasterFlareEntry]:
        return list(reversed(self._entries[-limit:]))

    def get_by_id(self, master_id: str) -> Optional[MasterFlareEntry]:
        for e in self._entries:
            if e.master_id == master_id:
                return e
        return None

    def search(self, query: str) -> List[MasterFlareEntry]:
        q = query.lower()
        return [e for e in self._entries if q in e.master_id.lower() or q in (e.quality or "").lower()]

    @property
    def total_count(self) -> int:
        return len(self._entries)

    @property
    def active_count(self) -> int:
        return len(self.get_active())

    def statistics(self) -> Dict:
        return {
            "total": self.total_count,
            "active": self.active_count,
            "completed": sum(1 for e in self._entries if e.phase in (FlarePhase.COMPLETED, FlarePhase.ARCHIVED)),
            "avg_confidence": sum(e.confidence for e in self._entries) / max(1, self.total_count),
            "avg_peak_flux": sum(e.peak_flux for e in self._entries) / max(1, self.total_count),
        }

    def export_json(self) -> str:
        return json.dumps([e.dict() for e in self._entries], indent=2, default=str)

    @property
    def all_entries(self) -> List[MasterFlareEntry]:
        return list(self._entries)
