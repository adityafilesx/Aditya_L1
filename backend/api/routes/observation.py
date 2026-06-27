from fastapi import APIRouter, HTTPException
from typing import List
from backend.observation_engine.observation_manager import observation_manager
from backend.observation_engine.models import EnrichedObservation

router = APIRouter()

@router.get("/current", response_model=EnrichedObservation)
async def get_current_observation():
    obs = observation_manager.repository.get_latest()
    if not obs:
        raise HTTPException(status_code=404, detail="No observation data available")
    return obs

@router.get("/history", response_model=List[EnrichedObservation])
async def get_observation_history(limit: int = 100):
    return observation_manager.repository.get_history(limit=limit)

@router.get("/{obs_id}", response_model=EnrichedObservation)
async def get_observation_by_id(obs_id: str):
    obs = observation_manager.repository.search_by_id(obs_id)
    if not obs:
        raise HTTPException(status_code=404, detail="Observation not found")
    return obs

@router.get("/pipeline/status")
async def get_pipeline_status():
    obs = observation_manager.repository.get_latest()
    if not obs:
        return {"status": "YELLOW", "detail": "Awaiting first observation"}
        
    status = "GREEN"
    if obs.quality.overall_scientific_confidence < 0.5:
        status = "RED"
    elif obs.quality.overall_scientific_confidence < 0.8:
        status = "YELLOW"
        
    return {
        "status": status,
        "last_updated": obs.timestamp,
        "observation_rate_hz": 1.0,
        "active_instruments": ["SoLEXS-1", "HEL1OS-1"],
        "current_latency_ms": obs.provenance.total_latency_ms,
        "system_health": "NOMINAL" if status == "GREEN" else "DEGRADED"
    }

@router.get("/export/csv")
async def export_observations():
    # Placeholder for CSV export
    return observation_manager.repository.export()
