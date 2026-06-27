"""
Context Builder — Automatically gathers full platform state for every reasoning request.

The user never needs to repeat context. The Context Builder reads from the
global AppState singleton to capture:
  - Digital Twin state (active regions, global solar state)
  - Knowledge Graph summary (nodes, edges, communities)
  - Latest telemetry
  - Latest physics parameters
  - Latest predictions and decision state
  - Mission intelligence (risk indices)
"""

import logging
import json
import time
from typing import Any, Dict, Optional

logger = logging.getLogger("SRE.ContextBuilder")


class ReasoningContext:
    """Structured platform context passed to every agent."""

    def __init__(
        self,
        timestamp: float,
        mission_time_utc: str,
        digital_twin: Dict[str, Any],
        active_regions: Dict[str, Any],
        knowledge_graph_summary: Dict[str, Any],
        telemetry: Dict[str, Any],
        physics: Dict[str, Any],
        predictions: Dict[str, Any],
        decision_state: Dict[str, Any],
        risk_indices: Dict[str, Any],
        # Optional user-supplied overrides
        selected_region_id: Optional[str] = None,
        selected_graph_node_id: Optional[str] = None,
        cursor_time: Optional[float] = None,
    ):
        self.timestamp = timestamp
        self.mission_time_utc = mission_time_utc
        self.digital_twin = digital_twin
        self.active_regions = active_regions
        self.knowledge_graph_summary = knowledge_graph_summary
        self.telemetry = telemetry
        self.physics = physics
        self.predictions = predictions
        self.decision_state = decision_state
        self.risk_indices = risk_indices
        self.selected_region_id = selected_region_id
        self.selected_graph_node_id = selected_graph_node_id
        self.cursor_time = cursor_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "mission_time_utc": self.mission_time_utc,
            "digital_twin": self.digital_twin,
            "active_regions": self.active_regions,
            "knowledge_graph_summary": self.knowledge_graph_summary,
            "telemetry": self.telemetry,
            "physics": self.physics,
            "predictions": self.predictions,
            "decision_state": self.decision_state,
            "risk_indices": self.risk_indices,
            "selected_region_id": self.selected_region_id,
            "selected_graph_node_id": self.selected_graph_node_id,
            "cursor_time": self.cursor_time,
        }

    def summary_text(self) -> str:
        """Human-readable summary of the current context for agent prompts."""
        lines = [
            f"**Mission Time**: {self.mission_time_utc}",
        ]
        if self.selected_region_id:
            lines.append(f"**Selected Region**: {self.selected_region_id}")
        if self.active_regions:
            ar_ids = list(self.active_regions.keys()) if isinstance(self.active_regions, dict) else []
            lines.append(f"**Active Regions**: {', '.join(str(a) for a in ar_ids[:5])}")
        if self.predictions:
            prob = self.predictions.get("probability", "N/A")
            cls = self.predictions.get("predicted_class", "N/A")
            lines.append(f"**Current Prediction**: {cls} (P={prob})")
        if self.risk_indices:
            risk = self.risk_indices.get("mission_risk_index", "N/A")
            lines.append(f"**Mission Risk Index**: {risk}")
        return "\n".join(lines)


class ContextBuilder:
    """
    Builds a ReasoningContext from the global AppState.
    Called at the start of every reasoning request.
    """

    def __init__(self, app_state):
        self.app_state = app_state

    def build(
        self,
        selected_region_id: Optional[str] = None,
        selected_graph_node_id: Optional[str] = None,
        cursor_time: Optional[float] = None,
    ) -> ReasoningContext:
        now = time.time()
        logger.info("Building reasoning context...")

        # ── Digital Twin ──
        try:
            twin_raw = self.app_state.digital_twin.get_full_state()
            digital_twin = json.loads(twin_raw) if isinstance(twin_raw, str) else twin_raw
        except Exception as e:
            logger.warning(f"Digital Twin context unavailable: {e}")
            digital_twin = {}

        try:
            active_regions = self.app_state.digital_twin.active_regions or {}
        except Exception:
            active_regions = {}

        # ── Knowledge Graph ──
        try:
            kg_summary = self.app_state.knowledge_graph.get_summary()
        except Exception as e:
            logger.warning(f"Knowledge Graph context unavailable: {e}")
            kg_summary = {}

        # ── Telemetry / Physics / Predictions ──
        telemetry = self.app_state.latest_telemetry or {}
        physics = self.app_state.latest_physics or {}
        predictions = self.app_state.latest_predictions or {}

        # ── Decision State ──
        try:
            from backend.api.mock_data import generate_mock_forecast
            pred_input = predictions if predictions else generate_mock_forecast()
            decision_state = self.app_state.decision_engine.evaluate(pred_input, telemetry)
        except Exception as e:
            logger.warning(f"Decision state unavailable: {e}")
            decision_state = {}

        # ── Risk Indices ──
        try:
            import torch
            dummy = torch.randn(1, 128)
            with torch.no_grad():
                preds = self.app_state.mission_intelligence(dummy)
            risk_indices = {
                "mission_risk_index": round(preds["mission_risk_index"].item(), 4),
                "radiation_context_index": round(preds["radiation_context_index"].item(), 4),
                "hf_blackout_risk_index": round(preds["hf_blackout_risk_index"].item(), 4),
            }
        except Exception as e:
            logger.warning(f"Risk indices unavailable: {e}")
            risk_indices = {}

        from datetime import datetime, timezone
        mission_time = datetime.fromtimestamp(cursor_time or now, tz=timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )

        ctx = ReasoningContext(
            timestamp=now,
            mission_time_utc=mission_time,
            digital_twin=digital_twin,
            active_regions=active_regions,
            knowledge_graph_summary=kg_summary,
            telemetry=telemetry,
            physics=physics,
            predictions=predictions,
            decision_state=decision_state,
            risk_indices=risk_indices,
            selected_region_id=selected_region_id,
            selected_graph_node_id=selected_graph_node_id,
            cursor_time=cursor_time,
        )
        logger.info(f"Reasoning context built ({len(ctx.to_dict())} fields)")
        return ctx
