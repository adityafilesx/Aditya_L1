from fastapi import APIRouter
from backend.api.state import app_state
from backend.api.mock_data import generate_mock_forecast
import time

router = APIRouter(prefix="/decision", tags=["decision"])

@router.get("/state")
async def get_state():
    """
    Returns the current operational state, confidence bounds, and recommendations.
    Evaluates the state machine dynamically if needed.
    """
    prediction_result = app_state.latest_predictions
    if not prediction_result:
        prediction_result = generate_mock_forecast()
        
    telemetry = app_state.latest_telemetry or {}
    
    # Evaluate decision engine
    context = app_state.decision_engine.evaluate(prediction_result, telemetry)
    return context

@router.get("/alerts")
async def get_alerts():
    """Returns active and recent alerts."""
    # Read from alert manager log if we wanted to show history,
    # or just return the active one from state.
    # For now, simulate reading the alert file or return a clean slate.
    return []

@router.get("/thresholds")
async def get_thresholds():
    """Returns the currently active dynamic thresholds."""
    return app_state.decision_engine.current_dynamic_thresholds or {}

@router.get("/drift")
async def get_drift():
    return app_state.decision_engine.drift_monitor.check_drift()
