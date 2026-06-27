"""
Event Timeline Engine.

Maintains active and historical event timelines with lifecycle progression
and replay support by time window.
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from typing import List, Optional

from backend.nowcasting.models import MasterFlareEntry, FlarePhase


class EventTimeline:
    """Maintains active and past event timelines."""

    def __init__(self, max_history: int = 100):
        self._active: List[MasterFlareEntry] = []
        self._history: deque[MasterFlareEntry] = deque(maxlen=max_history)
        self._all_events: deque[MasterFlareEntry] = deque(maxlen=500)

    def add_event(self, entry: MasterFlareEntry) -> None:
        self._active.append(entry)
        self._all_events.append(entry)

    def complete_event(self, master_id: str) -> None:
        completed = [e for e in self._active if e.master_id == master_id]
        self._active = [e for e in self._active if e.master_id != master_id]
        for e in completed:
            self._history.append(e)

    def get_active(self) -> List[MasterFlareEntry]:
        return list(self._active)

    def get_history(self, limit: int = 20) -> List[MasterFlareEntry]:
        entries = list(self._history)
        return entries[-limit:]

    def get_timeline(self, limit: int = 20) -> List[MasterFlareEntry]:
        """Return combined active + recent history for the timeline view."""
        return self._active + self.get_history(limit)

    def replay(self, start: Optional[str] = None, end: Optional[str] = None) -> List[MasterFlareEntry]:
        """Replay events within a time window."""
        results = []
        for e in self._all_events:
            if start and e.unified_start and e.unified_start < start:
                continue
            if end and e.unified_start and e.unified_start > end:
                continue
            results.append(e)
        return results

    @property
    def total_events(self) -> int:
        return len(self._all_events)
