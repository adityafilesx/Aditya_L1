"""
Tool Registry — Central registry mapping tool names to callable async functions.
Wraps existing AppState methods into a discoverable interface.
"""

import logging
import json
from typing import Any, Callable, Dict, Optional
from backend.api.state import app_state
from backend.api.mock_data import generate_mock_forecast, generate_mock_physics

logger = logging.getLogger("SRE.ToolRegistry")


class Tool:
    """A callable tool wrapping a platform capability."""

    def __init__(self, name: str, description: str, fn: Callable, module: str):
        self.name = name
        self.description = description
        self.fn = fn
        self.module = module

    async def __call__(self, **kwargs) -> Any:
        try:
            result = self.fn(**kwargs)
            return result
        except Exception as e:
            logger.error(f"Tool '{self.name}' failed: {e}")
            return {"error": str(e)}


def _physics_summary(**kwargs):
    if app_state.latest_physics:
        return app_state.latest_physics
    return generate_mock_physics()


def _forecast_current(**kwargs):
    if app_state.latest_predictions:
        return app_state.latest_predictions
    return generate_mock_forecast()


def _digital_twin_state(**kwargs):
    try:
        raw = app_state.digital_twin.get_full_state()
        return json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        return {}


def _digital_twin_regions(**kwargs):
    return app_state.digital_twin.active_regions or {}


def _digital_twin_similarity(ar_num: int = 0, **kwargs):
    return app_state.digital_twin.find_historical_similarity(ar_num)


def _knowledge_graph_summary(**kwargs):
    return app_state.knowledge_graph.get_summary()


def _knowledge_graph_events(**kwargs):
    return list(app_state.knowledge_graph.graph.nodes(data=True))


def _decision_state(**kwargs):
    pred = app_state.latest_predictions or generate_mock_forecast()
    tel = app_state.latest_telemetry or {}
    return app_state.decision_engine.evaluate(pred, tel)


def _decision_thresholds(**kwargs):
    return app_state.decision_engine.current_dynamic_thresholds or {}


# ── Registry ──

TOOL_REGISTRY: Dict[str, Tool] = {
    "physics_summary": Tool(
        "physics_summary",
        "Returns current physics engine parameters (temperature, EM, entropy, Neupert delay)",
        _physics_summary,
        "physics_engine",
    ),
    "forecast_current": Tool(
        "forecast_current",
        "Returns the latest flare prediction (probability, class, confidence)",
        _forecast_current,
        "ai_engine",
    ),
    "digital_twin_state": Tool(
        "digital_twin_state",
        "Returns the full Solar Digital Twin state",
        _digital_twin_state,
        "digital_twin",
    ),
    "digital_twin_regions": Tool(
        "digital_twin_regions",
        "Returns currently tracked active regions",
        _digital_twin_regions,
        "digital_twin",
    ),
    "digital_twin_similarity": Tool(
        "digital_twin_similarity",
        "Finds historical similarity for a given AR number",
        _digital_twin_similarity,
        "digital_twin",
    ),
    "knowledge_graph_summary": Tool(
        "knowledge_graph_summary",
        "Returns Knowledge Graph summary (node/edge counts, event types)",
        _knowledge_graph_summary,
        "knowledge_graph",
    ),
    "knowledge_graph_events": Tool(
        "knowledge_graph_events",
        "Returns all nodes in the Knowledge Graph",
        _knowledge_graph_events,
        "knowledge_graph",
    ),
    "decision_state": Tool(
        "decision_state",
        "Returns operational state, confidence bounds, recommendations",
        _decision_state,
        "decision",
    ),
    "decision_thresholds": Tool(
        "decision_thresholds",
        "Returns currently active dynamic thresholds",
        _decision_thresholds,
        "decision",
    ),
}


def get_tool(name: str) -> Optional[Tool]:
    return TOOL_REGISTRY.get(name)


def list_tools() -> list:
    return [
        {"name": t.name, "description": t.description, "module": t.module}
        for t in TOOL_REGISTRY.values()
    ]
