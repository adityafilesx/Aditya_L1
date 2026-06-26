import asyncio
from fastapi import APIRouter
from api.routes.operations import get_telemetry, get_physics, get_models_status, get_health
from api.routes.decision import get_state
from api.routes.forecast import get_current_forecast

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/")
async def get_dashboard():
    """
    Unified endpoint for the Mission Overview Dashboard.
    Aggregates data from multiple domains to reduce frontend requests.
    """
    # Run independent data fetches concurrently
    telemetry, physics, models, health, forecast = await asyncio.gather(
        get_telemetry(),
        get_physics(),
        get_models_status(),
        get_health(),
        get_current_forecast()
    )
    
    # State evaluates dynamically based on predictions and telemetry
    state = await get_state()
    
    return {
        "mission_state": state,
        "telemetry": telemetry,
        "physics_summary": physics,
        "forecast": forecast,
        "sensor_health": health,
        "models": models,
        "alerts": [] # Could pull from AlertManager
    }
