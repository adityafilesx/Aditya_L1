"""
Mission Agent — Queries MissionIntelligenceEngine for risk indices,
HF blackout, radiation, CME, SEP, and recommendations.
"""

import logging
from typing import Any
from backend.reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.MissionAgent")


class MissionAgent(BaseAgent):
    name = "mission"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        action = subtask.action

        if action == "get_status":
            return self._get_status(context)
        elif action == "get_risk":
            return self._get_risk(context)
        else:
            return self._get_status(context)

    def _get_status(self, context: Any) -> AgentResult:
        risk = context.risk_indices or {}
        decision = context.decision_state or {}
        predictions = context.predictions or {}

        op_state = decision.get("operational_state", "NOMINAL")
        mission_risk = risk.get("mission_risk_index", 0.0)
        radiation = risk.get("radiation_context_index", 0.0)
        hf_blackout = risk.get("hf_blackout_risk_index", 0.0)
        prob = predictions.get("probability", 0.0)
        cls = predictions.get("predicted_class", "Quiet")

        # Determine overall status
        if mission_risk > 0.7 or prob > 0.7:
            status_icon = "🔴"
            status_label = "HIGH ALERT"
        elif mission_risk > 0.4 or prob > 0.4:
            status_icon = "🟡"
            status_label = "ELEVATED"
        else:
            status_icon = "🟢"
            status_label = "NOMINAL"

        content = (
            f"### {status_icon} Mission Status: {status_label}\n\n"
            f"| Index | Value | Level |\n"
            f"|---|---|---|\n"
            f"| Mission Risk | {mission_risk:.3f} | {'High' if mission_risk > 0.7 else 'Moderate' if mission_risk > 0.4 else 'Low'} |\n"
            f"| Radiation Context | {radiation:.3f} | {'Elevated' if radiation > 0.5 else 'Normal'} |\n"
            f"| HF Blackout Risk | {hf_blackout:.3f} | {'Warning' if hf_blackout > 0.6 else 'Clear'} |\n\n"
            f"**Operational State**: {op_state}\n\n"
            f"**Current Flare Prediction**: {cls}-Class at {prob*100:.1f}% probability.\n"
        )

        return self._make_result(
            content=content,
            confidence=0.93,
            sources=[
                Source(title="Mission Intelligence Engine", module="mission_intelligence", id="risk"),
                Source(title="Decision Engine", module="decision", id="state"),
            ],
            data={"risk": risk, "operational_state": op_state},
        )

    def _get_risk(self, context: Any) -> AgentResult:
        risk = context.risk_indices or {}
        mission_risk = risk.get("mission_risk_index", 0.0)

        recommendations = []
        if mission_risk > 0.7:
            recommendations = [
                "Increase telemetry sampling rate to 1Hz",
                "Alert ground station operators",
                "Prepare contingency observation schedule",
                "Enable autonomous onboard trigger",
            ]
        elif mission_risk > 0.4:
            recommendations = [
                "Monitor active regions closely",
                "Review prediction ensemble agreement",
                "Pre-stage data downlink capacity",
            ]
        else:
            recommendations = [
                "Continue nominal operations",
                "Standard monitoring cadence",
            ]

        content = "### Mission Recommendations\n\n"
        for i, rec in enumerate(recommendations, 1):
            content += f"{i}. {rec}\n"

        return self._make_result(
            content=content,
            confidence=0.90,
            sources=[Source(title="Mission Intelligence", module="mission_intelligence", id="recommendations")],
            data={"recommendations": recommendations},
        )
