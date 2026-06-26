from fastapi import APIRouter
from api.state import app_state
from api.mock_data import generate_mock_forecast

router = APIRouter(prefix="/forecast", tags=["forecast"])

@router.get("/current")
async def get_current_forecast():
    """Returns the latest 15-minute ahead prediction from the models."""
    if not app_state.latest_predictions:
        return generate_mock_forecast()
    return app_state.latest_predictions

@router.get("/horizons")
async def get_horizons():
    """Returns predictions for multiple time horizons."""
    base = generate_mock_forecast()
    
    # Simulate decreasing probability for longer horizons if it's a flare,
    # or just variations.
    return {
        "15m": base,
        "30m": {**base, "probability": max(0, base["probability"] - 0.05), "confidence": 0.85},
        "1h": {**base, "probability": max(0, base["probability"] - 0.1), "confidence": 0.75},
        "3h": {**base, "probability": max(0, base["probability"] - 0.15), "confidence": 0.60},
        "6h": {**base, "probability": max(0, base["probability"] - 0.2), "confidence": 0.50}
    }
