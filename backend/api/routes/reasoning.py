"""
Reasoning API Routes — SSE streaming chat and analysis endpoints.

POST /api/reasoning/chat     — SSE streaming chat
POST /api/reasoning/analyze  — Deep analysis (non-streaming)
POST /api/reasoning/report   — Generate full mission report
POST /api/reasoning/compare  — Compare events
GET  /api/reasoning/context  — Current platform context
GET  /api/reasoning/history  — Conversation history
"""

import json
import logging
from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from reasoning.reasoner import ScientificReasoner
from api.state import app_state

logger = logging.getLogger("SRE.API")

router = APIRouter(prefix="/reasoning", tags=["reasoning"])

# ── Initialize the Scientific Reasoner ──
_reasoner: Optional[ScientificReasoner] = None


def get_reasoner() -> ScientificReasoner:
    global _reasoner
    if _reasoner is None:
        _reasoner = ScientificReasoner(app_state)
    return _reasoner


# ── Request Models ──

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    selected_region_id: Optional[str] = None
    selected_graph_node_id: Optional[str] = None
    cursor_time: Optional[float] = None


class AnalyzeRequest(BaseModel):
    query: str
    selected_region_id: Optional[str] = None
    selected_graph_node_id: Optional[str] = None
    cursor_time: Optional[float] = None


# ── Endpoints ──

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    SSE streaming chat endpoint.
    Streams reasoning chunks as Server-Sent Events.
    """
    reasoner = get_reasoner()

    async def event_stream():
        async for chunk in reasoner.reason_stream(
            query=request.query,
            session_id=request.session_id,
            selected_region_id=request.selected_region_id,
            selected_graph_node_id=request.selected_graph_node_id,
            cursor_time=request.cursor_time,
        ):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    """Deep analysis endpoint (non-streaming). Returns full response at once."""
    reasoner = get_reasoner()
    result = await reasoner.reason(
        query=request.query,
        selected_region_id=request.selected_region_id,
        selected_graph_node_id=request.selected_graph_node_id,
        cursor_time=request.cursor_time,
    )
    return result


@router.post("/report")
async def generate_report(request: AnalyzeRequest):
    """Generate a full mission report."""
    reasoner = get_reasoner()
    result = await reasoner.reason(
        query="/report " + request.query,
        selected_region_id=request.selected_region_id,
        cursor_time=request.cursor_time,
    )
    return result


@router.post("/compare")
async def compare(request: AnalyzeRequest):
    """Compare events or predictions."""
    reasoner = get_reasoner()
    result = await reasoner.reason(
        query="/compare " + request.query,
        selected_region_id=request.selected_region_id,
        cursor_time=request.cursor_time,
    )
    return result


@router.get("/context")
async def get_context(
    selected_region_id: Optional[str] = None,
    selected_graph_node_id: Optional[str] = None,
    cursor_time: Optional[float] = None,
):
    """Returns the current full platform context."""
    reasoner = get_reasoner()
    return reasoner.get_context(
        selected_region_id=selected_region_id,
        selected_graph_node_id=selected_graph_node_id,
        cursor_time=cursor_time,
    )


@router.get("/history")
async def get_history(session_id: Optional[str] = None, limit: int = 50):
    """Returns conversation history."""
    reasoner = get_reasoner()
    return reasoner.get_history(session_id, limit)
