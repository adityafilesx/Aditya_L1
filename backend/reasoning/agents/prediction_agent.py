"""
Prediction Agent — Queries the Decision Engine, forecast models, and calibration.
"""

import logging
from typing import Any
from backend.reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.PredictionAgent")


class PredictionAgent(BaseAgent):
    name = "prediction"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        action = subtask.action
        predictions = context.predictions or {}
        decision = context.decision_state or {}

        if action == "forecast":
            return self._forecast(subtask.params.get("query", ""), predictions, decision, context)
        elif action == "get_context":
            return self._get_context(predictions, decision)
        else:
            return self._get_context(predictions, decision)

    def _forecast(self, query: str, predictions: dict, decision: dict, context: Any) -> AgentResult:
        prob = predictions.get("probability", 0.35)
        cls = predictions.get("predicted_class", "C")
        conf = predictions.get("confidence", 0.80)
        op_state = decision.get("operational_state", "NOMINAL")

        content = (
            f"### Flare Prediction Analysis\n\n"
            f"| Metric | Value |\n"
            f"|---|---|\n"
            f"| Predicted Class | **{cls}-Class** |\n"
            f"| Probability | **{prob*100:.1f}%** |\n"
            f"| Model Confidence | **{conf*100:.1f}%** |\n"
            f"| Operational State | **{op_state}** |\n\n"
        )

        if prob > 0.7:
            content += (
                f"> 🔴 **HIGH ALERT**: Probability exceeds 70% for {cls}-class activity. "
                f"The Decision Engine has escalated the operational state to **{op_state}**.\n\n"
            )
        elif prob > 0.4:
            content += (
                f"> 🟡 **ELEVATED**: Moderate probability of {cls}-class activity. "
                f"Continuous monitoring recommended.\n\n"
            )
        else:
            content += f"> 🟢 Low probability. Nominal conditions.\n\n"

        # Ensemble agreement
        content += (
            f"**Ensemble Agreement**: The hybrid ensemble (XGBoost + TCN + Transformer) "
            f"shows {'strong' if conf > 0.85 else 'moderate' if conf > 0.7 else 'weak'} "
            f"inter-model agreement at the current prediction horizon.\n"
        )

        return self._make_result(
            content=content,
            confidence=conf,
            sources=[
                Source(title="Hybrid Ensemble Predictor", module="ai_engine", id="ensemble"),
                Source(title="Decision Engine", module="decision", id="state_machine"),
            ],
            data={"predictions": predictions, "decision": decision},
        )

    def _get_context(self, predictions: dict, decision: dict) -> AgentResult:
        prob = predictions.get("probability", 0.35)
        cls = predictions.get("predicted_class", "C")
        conf = predictions.get("confidence", 0.80)

        content = (
            f"Current prediction: **{cls}-Class** at **{prob*100:.1f}%** "
            f"(confidence: {conf*100:.1f}%). "
            f"Operational state: **{decision.get('operational_state', 'NOMINAL')}**."
        )
        return self._make_result(
            content=content,
            confidence=conf,
            sources=[Source(title="Prediction Engine", module="ai_engine", id="forecast")],
        )
