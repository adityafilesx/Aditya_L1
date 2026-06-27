"""
REST API endpoints for the Scientific Nowcasting Engine.

All endpoints are mounted under ``/api/nowcasting``.
"""

from __future__ import annotations

from fastapi import APIRouter, Query
from typing import Optional

from backend.nowcasting.manager import nowcast_manager

router = APIRouter(tags=["nowcasting"])


@router.get("/state")
async def get_nowcast_state():
    """Current complete NowcastState snapshot."""
    return nowcast_manager.get_state().dict()


@router.get("/catalog")
async def get_catalog():
    """Full Master Flare Catalog (last 50 entries)."""
    return [e.dict() for e in nowcast_manager.catalog.get_history(50)]


@router.get("/catalog/active")
async def get_active_catalog():
    """Currently active flare catalog entries."""
    return [e.dict() for e in nowcast_manager.catalog.get_active()]


@router.get("/catalog/{master_id}")
async def get_catalog_entry(master_id: str):
    """Single catalog entry by Master Flare ID."""
    entry = nowcast_manager.catalog.get_by_id(master_id)
    if entry:
        return entry.dict()
    return {"error": "Not found"}


@router.get("/detector/solexs")
async def get_solexs_detector():
    """SoLEXS detector snapshot."""
    return nowcast_manager.solexs_detector.snapshot().dict()


@router.get("/detector/helios")
async def get_helios_detector():
    """HEL1OS detector snapshot."""
    return nowcast_manager.helios_detector.snapshot().dict()


@router.get("/timeline")
async def get_timeline():
    """Current event timeline."""
    return [e.dict() for e in nowcast_manager.timeline.get_timeline(20)]


@router.get("/timeline/replay")
async def replay_timeline(
    start: Optional[str] = Query(None),
    end: Optional[str] = Query(None),
):
    """Replay events within a time window."""
    return [e.dict() for e in nowcast_manager.timeline.replay(start, end)]


@router.get("/repository/statistics")
async def get_statistics():
    """Event statistics."""
    return nowcast_manager.repository.get_statistics()


@router.get("/repository/export")
async def export_repository():
    """Export all events as JSON."""
    return nowcast_manager.repository.get_history(100)
