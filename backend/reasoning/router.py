"""
Router — Dispatches SubTask objects to the correct specialized agent.
Collects AgentResult objects and handles timeouts/fallbacks.
"""

import logging
import asyncio
from typing import Any, Dict, List

from reasoning.planner import SubTask
from reasoning.agents.base_agent import BaseAgent, AgentResult

logger = logging.getLogger("SRE.Router")


class Router:
    """Routes subtasks to registered agents and collects results."""

    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}

    def register(self, agent: BaseAgent):
        self.agents[agent.name] = agent
        logger.info(f"Registered agent: {agent.name}")

    async def dispatch(self, subtask: SubTask, context: Any) -> AgentResult:
        agent = self.agents.get(subtask.agent)
        if not agent:
            logger.warning(f"No agent registered for '{subtask.agent}'")
            return AgentResult(
                agent_name=subtask.agent,
                content=f"Agent '{subtask.agent}' is not available.",
                confidence=0.0,
                warnings=[f"Missing agent: {subtask.agent}"],
            )

        try:
            result = await asyncio.wait_for(
                agent.execute(subtask, context),
                timeout=10.0,  # 10-second timeout per agent
            )
            logger.info(
                f"Agent '{subtask.agent}' completed "
                f"(confidence={result.confidence:.2f}, "
                f"content_len={len(result.content)})"
            )
            return result
        except asyncio.TimeoutError:
            logger.error(f"Agent '{subtask.agent}' timed out")
            return AgentResult(
                agent_name=subtask.agent,
                content=f"Agent '{subtask.agent}' timed out after 10 seconds.",
                confidence=0.0,
                warnings=[f"Timeout: {subtask.agent}"],
            )
        except Exception as e:
            logger.error(f"Agent '{subtask.agent}' failed: {e}")
            return AgentResult(
                agent_name=subtask.agent,
                content=f"Agent '{subtask.agent}' encountered an error: {str(e)}",
                confidence=0.0,
                warnings=[f"Error in {subtask.agent}: {str(e)}"],
            )

    async def dispatch_plan(self, subtasks: List[SubTask], context: Any) -> List[AgentResult]:
        """Execute all subtasks in order, collecting results."""
        results: List[AgentResult] = []
        for subtask in subtasks:
            # Pass prior results to the review agent
            if subtask.agent == "review":
                subtask.params["prior_results"] = results
            result = await self.dispatch(subtask, context)
            results.append(result)
        return results
