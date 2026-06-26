from fastapi import APIRouter
from api.state import app_state

router = APIRouter(prefix="/knowledge-graph", tags=["knowledge-graph"])

@router.get("/")
async def get_summary():
    """Returns a summary of the Event Knowledge Graph."""
    return app_state.knowledge_graph.get_summary()

@router.get("/events")
async def get_events():
    """Returns all nodes in the Knowledge Graph."""
    # Returns a list of nodes with their data
    return list(app_state.knowledge_graph.graph.nodes(data=True))
