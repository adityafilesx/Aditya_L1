from fastapi import APIRouter
from typing import Dict, Any
from backend.forecasting.forecast_repository.repository import forecast_repository
from backend.forecasting.timeline.evolution import evolution_tracker

router = APIRouter(prefix="/api/forecast", tags=["forecast"])

@router.get("/current")
def get_current_forecast():
    # Return the latest forecast from the repository
    all_f = forecast_repository.get_all()
    if not all_f:
        return {"status": "No forecasts available."}
    return all_f[-1]

@router.get("/history")
def get_forecast_history():
    return forecast_repository.get_all()

@router.get("/timeline")
def get_forecast_timeline():
    return evolution_tracker.get_timeline()
