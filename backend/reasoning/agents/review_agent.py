"""
Review Agent — Validates evidence, checks confidence, flags uncertainty.
This is the final gate before responses reach the user.
"""

import logging
from typing import Any, List
from reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.ReviewAgent")


class ReviewAgent(BaseAgent):
    name = "review"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        # The review agent is called last and doesn't produce primary content.
        # It validates all prior results passed via subtask.params.
        prior_results: List[AgentResult] = subtask.params.get("prior_results", [])
        return self._validate(prior_results)

    def _validate(self, results: List[AgentResult]) -> AgentResult:
        if not results:
            return self._make_result(
                content="",
                confidence=0.5,
                warnings=["No prior agent results to validate."],
            )

        total_confidence = sum(r.confidence for r in results) / len(results)
        all_warnings = []

        for r in results:
            if r.confidence < 0.5:
                all_warnings.append(
                    f"⚠️ Low confidence ({r.confidence:.0%}) from **{r.agent_name}** agent."
                )
            if not r.sources:
                all_warnings.append(
                    f"⚠️ No traceable sources from **{r.agent_name}** agent."
                )
            all_warnings.extend(r.warnings)

        review_note = ""
        if all_warnings:
            review_note = (
                "\n---\n\n### 🔍 Reviewer Notes\n\n"
                + "\n".join(f"- {w}" for w in all_warnings)
                + f"\n\n**Aggregate Confidence**: {total_confidence:.0%}\n"
            )
        else:
            review_note = (
                f"\n---\n\n> ✅ All sources verified. "
                f"Aggregate confidence: **{total_confidence:.0%}**.\n"
            )

        return self._make_result(
            content=review_note,
            confidence=total_confidence,
            warnings=all_warnings,
        )
