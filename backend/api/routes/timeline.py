from fastapi import APIRouter
import random
from datetime import datetime, timedelta, timezone

router = APIRouter(prefix="/timeline", tags=["timeline"])

@router.get("/events")
async def get_events():
    """Returns a list of recent mission events (simulated for now)."""
    now = datetime.now(timezone.utc)
    return [
        {
            "id": "EVT-1",
            "timestamp": (now - timedelta(minutes=15)).isoformat(),
            "type": "FLARE_START",
            "description": "M1.2 flare onset detected in AR12673",
            "severity": "high"
        },
        {
            "id": "EVT-2",
            "timestamp": (now - timedelta(minutes=45)).isoformat(),
            "type": "SYSTEM",
            "description": "Telemetry switched to high-rate mode",
            "severity": "info"
        },
        {
            "id": "EVT-3",
            "timestamp": (now - timedelta(hours=2)).isoformat(),
            "type": "DATA_GAP",
            "description": "Brief 30s telemetry dropout on X-band",
            "severity": "warning"
        }
    ]

@router.get("/alerts")
async def get_timeline_alerts():
    return []
