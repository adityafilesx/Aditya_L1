from fastapi import APIRouter
from api.state import app_state
from api.mock_data import generate_mock_physics

router = APIRouter(prefix="/physics", tags=["physics"])

@router.get("/summary")
async def get_summary():
    """Returns physics engine summary."""
    if not app_state.latest_physics:
        return generate_mock_physics()
    return app_state.latest_physics
