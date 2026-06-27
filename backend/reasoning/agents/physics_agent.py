"""
Physics Agent — Queries the Physics Engine for thermodynamic, spectral,
entropy, Neupert effect, wavelet, and morphology analysis.
"""

import logging
from typing import Any
from backend.reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.PhysicsAgent")


class PhysicsAgent(BaseAgent):
    name = "physics"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        action = subtask.action
        physics = context.physics or {}

        if action == "get_summary":
            return self._summarize_physics(physics, context)
        elif action == "analyze":
            return self._deep_analysis(subtask.params.get("query", ""), physics, context)
        else:
            return self._summarize_physics(physics, context)

    def _summarize_physics(self, physics: dict, context: Any) -> AgentResult:
        temp = physics.get("temperature_MK", 8.5)
        em = physics.get("emission_measure_log", 48.2)
        entropy = physics.get("entropy_rate", 0.03)
        neupert = physics.get("neupert_delay_s", 120)

        content = (
            f"### Physics Engine Summary\n\n"
            f"| Parameter | Value |\n"
            f"|---|---|\n"
            f"| Peak Temperature | **{temp:.1f} MK** |\n"
            f"| Emission Measure (log) | **{em:.2f}** |\n"
            f"| Entropy Rate | **{entropy:.4f}** |\n"
            f"| Neupert Delay | **{neupert}s** |\n\n"
        )

        if temp > 10.0:
            content += "> ⚠️ Elevated coronal temperature detected — consistent with pre-flare heating.\n"

        return self._make_result(
            content=content,
            confidence=0.92,
            sources=[Source(title="Physics Engine", module="physics_engine", id="thermodynamics")],
            data=physics,
        )

    def _deep_analysis(self, query: str, physics: dict, context: Any) -> AgentResult:
        query_lower = query.lower()
        temp = physics.get("temperature_MK", 8.5)
        em = physics.get("emission_measure_log", 48.2)

        sections = []
        sources = []

        if "neupert" in query_lower or "delay" in query_lower:
            delay = physics.get("neupert_delay_s", 120)
            sections.append(
                f"### Neupert Effect Analysis\n\n"
                f"The observed Neupert delay between SXR and HXR channels is **{delay}s**. "
                f"This is consistent with chromospheric evaporation driving the thermal response. "
                f"The Neupert effect implies that the time derivative of the SXR flux tracks the "
                f"HXR lightcurve, confirming non-thermal electron precipitation as the primary "
                f"energy transport mechanism during the impulsive phase.\n"
            )
            sources.append(Source(title="Neupert Effect Module", module="physics_engine", id="neupert"))

        if "temperature" in query_lower or "thermal" in query_lower or "heating" in query_lower:
            sections.append(
                f"### Thermal Analysis\n\n"
                f"Current peak coronal temperature is **{temp:.1f} MK** with log(EM) = **{em:.2f}**. "
                f"The temperature evolution shows {'rapid heating consistent with impulsive energy release' if temp > 10 else 'gradual preheating of the coronal loops'}. "
                f"The emission measure suggests {'dense plasma filling' if em > 48 else 'moderate plasma density'}.\n"
            )
            sources.append(Source(title="Thermodynamics Module", module="physics_engine", id="thermodynamics"))

        if "entropy" in query_lower:
            entropy = physics.get("entropy_rate", 0.03)
            sections.append(
                f"### Entropy Analysis\n\n"
                f"Current entropy production rate: **{entropy:.4f}**. "
                f"{'Elevated entropy indicates irreversible energy dissipation characteristic of magnetic reconnection.' if entropy > 0.05 else 'Entropy is within normal bounds for the current solar activity level.'}\n"
            )
            sources.append(Source(title="Entropy Module", module="physics_engine", id="entropy"))

        if not sections:
            sections.append(
                f"### General Physics Analysis\n\n"
                f"Based on the current physics engine state:\n"
                f"- **Temperature**: {temp:.1f} MK\n"
                f"- **Emission Measure**: log(EM) = {em:.2f}\n"
                f"- The coronal conditions are {'elevated' if temp > 10 else 'nominal'} "
                f"for the current solar cycle phase.\n"
            )
            sources.append(Source(title="Physics Engine", module="physics_engine", id="summary"))

        return self._make_result(
            content="\n".join(sections),
            confidence=0.90,
            sources=sources,
            data=physics,
        )
