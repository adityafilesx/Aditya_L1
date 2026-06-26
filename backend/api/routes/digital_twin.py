import json
from fastapi import APIRouter
from api.state import app_state

router = APIRouter(prefix="/digital-twin", tags=["digital-twin"])

@router.get("/state")
async def get_state():
    """Returns the full Solar Digital Twin state as JSON."""
    twin_state_str = app_state.digital_twin.get_full_state()
    # The twin returns a JSON string, we want to return a dict for FastAPI
    try:
        return json.loads(twin_state_str)
    except Exception:
        return {"global_state": {}, "active_regions": {}}

@router.get("/active-regions")
async def get_active_regions():
    """Returns only the currently tracked active regions."""
    return app_state.digital_twin.active_regions

@router.get("/similarity/{ar_num}")
async def get_similarity(ar_num: int):
    """Finds historical similarity for a given active region."""
    return app_state.digital_twin.find_historical_similarity(ar_num)
