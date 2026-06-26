"""
Scientific Reasoner — Top-level orchestrator for the reasoning pipeline.

Pipeline:
  User Query
    → Context Builder
    → Planner
    → Router → Agents
    → Reviewer
    → Response Builder
    → Frontend (SSE stream)
"""

import logging
import time
from typing import Any, AsyncGenerator, Dict, List, Optional

from reasoning.context_builder import ContextBuilder, ReasoningContext
from reasoning.planner import Planner, Plan
from reasoning.router import Router
from reasoning.memory import ResearchMemory
from reasoning.agents.base_agent import AgentResult, Source

# Import all agents
from reasoning.agents.physics_agent import PhysicsAgent
from reasoning.agents.prediction_agent import PredictionAgent
from reasoning.agents.digital_twin_agent import DigitalTwinAgent
from reasoning.agents.knowledge_graph_agent import KnowledgeGraphAgent
from reasoning.agents.mission_agent import MissionAgent
from reasoning.agents.spectral_agent import SpectralAgent
from reasoning.agents.literature_agent import LiteratureAgent
from reasoning.agents.experiment_agent import ExperimentAgent
from reasoning.agents.report_agent import ReportAgent
from reasoning.agents.review_agent import ReviewAgent

logger = logging.getLogger("SRE.Reasoner")


class ScientificReasoner:
    """
    The main entry point for all scientific reasoning.
    Instantiated once at API startup and shared across requests.
    """

    def __init__(self, app_state):
        self.app_state = app_state

        # ── Core modules ──
        self.context_builder = ContextBuilder(app_state)
        self.planner = Planner()
        self.router = Router()
        self.memory = ResearchMemory()

        # ── Register all agents ──
        self.router.register(PhysicsAgent(app_state))
        self.router.register(PredictionAgent(app_state))
        self.router.register(DigitalTwinAgent(app_state))
        self.router.register(KnowledgeGraphAgent(app_state))
        self.router.register(MissionAgent(app_state))
        self.router.register(SpectralAgent(app_state))
        self.router.register(LiteratureAgent(app_state))
        self.router.register(ExperimentAgent(app_state))
        self.router.register(ReportAgent(app_state))
        self.router.register(ReviewAgent(app_state))

        logger.info("Scientific Reasoner initialized with 10 agents.")

    async def reason(
        self,
        query: str,
        session_id: Optional[str] = None,
        selected_region_id: Optional[str] = None,
        selected_graph_node_id: Optional[str] = None,
        cursor_time: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Full synchronous reasoning pipeline.
        Returns a complete response dict.
        """
        start = time.time()

        # 1. Build context
        context = self.context_builder.build(
            selected_region_id=selected_region_id,
            selected_graph_node_id=selected_graph_node_id,
            cursor_time=cursor_time,
        )

        # 2. Plan
        plan = self.planner.create_plan(query, context)

        # 3. Route & execute
        results = await self.router.dispatch_plan(plan.subtasks, context)

        # 4. Build response
        response = self._build_response(query, plan, results, context)

        # 5. Store in memory
        self.memory.add_message("user", query, session_id)
        self.memory.add_message(
            "ai",
            response["content"],
            session_id,
            metadata={
                "confidence": response["confidence"],
                "sources": response["sources"],
                "intent": plan.intent,
            },
        )

        elapsed = time.time() - start
        logger.info(f"Reasoning completed in {elapsed:.2f}s (intent={plan.intent})")
        response["elapsed_seconds"] = round(elapsed, 3)

        return response

    async def reason_stream(
        self,
        query: str,
        session_id: Optional[str] = None,
        selected_region_id: Optional[str] = None,
        selected_graph_node_id: Optional[str] = None,
        cursor_time: Optional[float] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Streaming reasoning pipeline.
        Yields markdown chunks as agents complete their work.
        """
        import json as _json

        # 1. Build context
        context = self.context_builder.build(
            selected_region_id=selected_region_id,
            selected_graph_node_id=selected_graph_node_id,
            cursor_time=cursor_time,
        )

        # 2. Plan
        plan = self.planner.create_plan(query, context)

        # Yield plan info
        yield _json.dumps({
            "type": "plan",
            "intent": plan.intent,
            "summary": plan.summary,
            "agent_count": len(plan.subtasks),
        })

        # 3. Execute agents one at a time, streaming each result
        all_results: List[AgentResult] = []
        for subtask in plan.subtasks:
            if subtask.agent == "review":
                subtask.params["prior_results"] = all_results

            result = await self.router.dispatch(subtask, context)
            all_results.append(result)

            # Stream agent result
            if result.content.strip():
                yield _json.dumps({
                    "type": "agent_result",
                    "agent": result.agent_name,
                    "content": result.content,
                    "confidence": result.confidence,
                    "sources": [
                        {"title": s.title, "module": s.module, "id": s.id}
                        for s in result.sources
                    ],
                })

        # 4. Final metadata
        avg_confidence = (
            sum(r.confidence for r in all_results) / len(all_results)
            if all_results
            else 0.0
        )
        all_sources = []
        for r in all_results:
            all_sources.extend(
                {"title": s.title, "module": s.module, "id": s.id}
                for s in r.sources
            )

        yield _json.dumps({
            "type": "complete",
            "confidence": round(avg_confidence, 3),
            "sources": all_sources,
            "intent": plan.intent,
        })

        # 5. Store in memory
        full_content = "\n\n".join(r.content for r in all_results if r.content.strip())
        self.memory.add_message("user", query, session_id)
        self.memory.add_message(
            "ai",
            full_content,
            session_id,
            metadata={"confidence": avg_confidence, "intent": plan.intent},
        )

    def get_context(
        self,
        selected_region_id: Optional[str] = None,
        selected_graph_node_id: Optional[str] = None,
        cursor_time: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Return the current platform context as a dict."""
        ctx = self.context_builder.build(
            selected_region_id=selected_region_id,
            selected_graph_node_id=selected_graph_node_id,
            cursor_time=cursor_time,
        )
        return ctx.to_dict()

    def get_history(self, session_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        return self.memory.get_history(session_id, limit)

    def _build_response(
        self,
        query: str,
        plan: Plan,
        results: List[AgentResult],
        context: ReasoningContext,
    ) -> Dict[str, Any]:
        """Merge all agent results into a single response."""
        # Combine all content
        sections = [r.content for r in results if r.content.strip()]
        content = "\n\n".join(sections)

        # Aggregate confidence
        confidences = [r.confidence for r in results if r.confidence > 0]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Aggregate sources (deduplicate)
        seen = set()
        sources = []
        for r in results:
            for s in r.sources:
                key = f"{s.module}:{s.id}"
                if key not in seen:
                    seen.add(key)
                    sources.append({"title": s.title, "module": s.module, "id": s.id})

        # Aggregate warnings
        warnings = []
        for r in results:
            warnings.extend(r.warnings)

        return {
            "content": content,
            "confidence": round(avg_confidence, 3),
            "sources": sources,
            "warnings": warnings,
            "intent": plan.intent,
            "plan_summary": plan.summary,
            "agent_count": len(plan.subtasks),
        }
