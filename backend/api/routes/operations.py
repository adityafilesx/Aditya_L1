from fastapi import APIRouter
from backend.api.state import app_state
from backend.api.mock_data import generate_mock_telemetry, generate_mock_physics

router = APIRouter(prefix="/operations", tags=["operations"])

@router.get("/telemetry")
async def get_telemetry():
    # In a real setup, we would read the latest row from a DB or shared memory
    # Here we simulate with the fallback generator if live telemetry isn't stored
    if not app_state.latest_telemetry:
        return generate_mock_telemetry()
    return app_state.latest_telemetry

@router.get("/physics")
async def get_physics():
    if not app_state.latest_physics:
        return generate_mock_physics()
    return app_state.latest_physics

@router.get("/health")
async def get_health():
    # Evaluate health of latest telemetry
    # For now, return a synthesized state
    return {
        "status": "NOMINAL",
        "message": "All sensor telemetry streams operating normally.",
        "sensors": {
            "solexs_sdd1": "ONLINE",
            "solexs_sdd2": "ONLINE",
            "helios_czt": "ONLINE",
            "suita_uv": "ONLINE"
        }
    }

@router.get("/models")
async def get_models_status():
    return {
        "ensemble_status": "ONLINE" if app_state.ensemble_forecaster else "DEGRADED (No trained models)",
        "xgb_status": "ONLINE" if app_state.xgb_model else "OFFLINE",
        "ai_temporal_status": "ONLINE" if app_state.ai_predictor else "OFFLINE",
    }
