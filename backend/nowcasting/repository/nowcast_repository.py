"""
Nowcast Repository.

In-memory event store supporting latest, history, search, statistics, and
JSON export.  Serves as the persistence layer for the nowcasting engine
(future milestones may back this with a database).
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional, Dict
import json

from backend.nowcasting.models import MasterFlareEntry


class NowcastRepository:
    """In-memory repository for nowcast events."""

    def __init__(self, max_size: int = 500):
        self._events: deque[MasterFlareEntry] = deque(maxlen=max_size)

    def store(self, entry: MasterFlareEntry) -> None:
        self._events.append(entry)

    def get_latest(self, n: int = 1) -> List[MasterFlareEntry]:
        entries = list(self._events)
        return entries[-n:]

    def get_history(self, limit: int = 50) -> List[MasterFlareEntry]:
        return list(reversed(list(self._events)[-limit:]))

    def search(self, query: str) -> List[MasterFlareEntry]:
        q = query.lower()
        return [e for e in self._events if q in e.master_id.lower()]

    def get_statistics(self) -> Dict:
        total = len(self._events)
        if total == 0:
            return {"total": 0, "avg_confidence": 0.0, "avg_peak_flux": 0.0}
        return {
            "total": total,
            "avg_confidence": sum(e.confidence for e in self._events) / total,
            "avg_peak_flux": sum(e.peak_flux for e in self._events) / total,
        }

    def export_json(self) -> str:
        return json.dumps([e.dict() for e in self._events], indent=2, default=str)

    def replay(self, start: Optional[str] = None, end: Optional[str] = None) -> List[MasterFlareEntry]:
        results = []
        for e in self._events:
            if start and e.unified_start and e.unified_start < start:
                continue
            if end and e.unified_start and e.unified_start > end:
                continue
            results.append(e)
        return results
