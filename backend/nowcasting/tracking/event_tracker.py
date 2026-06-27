"""
Active Event Tracker.

Tracks all currently active flares with real-time metrics:
elapsed time, growth rate, peak progress, and lifecycle state.
"""

from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, List

from backend.nowcasting.models import MasterFlareEntry, FlarePhase


class TrackedFlare:
    """Runtime tracking state for a single active flare."""

    def __init__(self, entry: MasterFlareEntry):
        self.master_id = entry.master_id
        self.entry = entry
        self._start = datetime.utcnow()

    @property
    def elapsed_seconds(self) -> float:
        return (datetime.utcnow() - self._start).total_seconds()

    @property
    def current_phase(self) -> FlarePhase:
        return self.entry.phase

    def to_dict(self) -> Dict:
        return {
            "master_id": self.master_id,
            "elapsed_s": round(self.elapsed_seconds, 1),
            "phase": self.entry.phase.value,
            "peak_flux": self.entry.peak_flux,
            "confidence": self.entry.confidence,
        }


class EventTracker:
    """Manages all currently active flares."""

    def __init__(self):
        self._active: Dict[str, TrackedFlare] = {}

    def track(self, entry: MasterFlareEntry) -> None:
        self._active[entry.master_id] = TrackedFlare(entry)

    def untrack(self, master_id: str) -> None:
        self._active.pop(master_id, None)

    def update(self, entry: MasterFlareEntry) -> None:
        if entry.master_id in self._active:
            self._active[entry.master_id].entry = entry

    def get_active(self) -> List[TrackedFlare]:
        return list(self._active.values())

    @property
    def active_count(self) -> int:
        return len(self._active)

    def cleanup_completed(self) -> List[str]:
        """Remove flares that have moved to COMPLETED or ARCHIVED."""
        to_remove = [
            mid for mid, t in self._active.items()
            if t.entry.phase in (FlarePhase.COMPLETED, FlarePhase.ARCHIVED)
        ]
        for mid in to_remove:
            del self._active[mid]
        return to_remove
