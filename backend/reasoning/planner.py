"""
Planner Agent — Understands intent, decomposes queries into subtasks, and assigns agents.

The Planner NEVER answers directly. It always delegates to specialized agents
via SubTask objects routed through the Tool Router.

Intent Classification:
  - explain     → Physics/Spectral Agent
  - predict     → Prediction Agent
  - compare     → Knowledge Graph Agent + Digital Twin Agent
  - report      → Report Agent (orchestrates all others)
  - literature  → Literature Agent
  - experiment  → Experiment Agent
  - mission     → Mission Agent
  - general     → Multi-agent synthesis
"""

import logging
import re
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

logger = logging.getLogger("SRE.Planner")


@dataclass
class SubTask:
    """A single unit of work assigned to a specialized agent."""
    agent: str           # e.g. "physics", "prediction", "digital_twin"
    action: str          # e.g. "get_temperature", "explain_neupert"
    params: Dict[str, Any] = field(default_factory=dict)
    priority: int = 0    # Lower = higher priority
    depends_on: Optional[str] = None  # ID of a subtask this depends on


@dataclass
class Plan:
    """An ordered sequence of subtasks that constitute a reasoning plan."""
    intent: str
    subtasks: List[SubTask]
    summary: str  # Human-readable plan description


# ── Keyword-based intent classification ──
INTENT_PATTERNS = {
    "explain": [
        r"why\b", r"explain\b", r"how does", r"what caused", r"reason\b",
        r"neupert", r"heating", r"cooling", r"entropy", r"emission measure",
        r"temperature", r"spectral", r"physics", r"mechanism",
    ],
    "predict": [
        r"predict\b", r"forecast\b", r"probability", r"will there be",
        r"chance of", r"confidence\b", r"calibration", r"nowcast",
        r"next flare", r"upcoming",
    ],
    "compare": [
        r"compare\b", r"similar\b", r"difference\b", r"historical",
        r"previous event", r"like this", r"vs\b", r"versus",
    ],
    "report": [
        r"/report\b", r"generate report", r"mission summary",
        r"write a report", r"publish", r"document\b",
    ],
    "literature": [
        r"/literature\b", r"paper\b", r"research\b", r"citation",
        r"arxiv", r"nasa ads", r"publication", r"journal",
    ],
    "experiment": [
        r"experiment\b", r"benchmark\b", r"model comparison",
        r"training\b", r"hyperparameter", r"dataset\b",
    ],
    "mission": [
        r"mission\b", r"status\b", r"risk\b", r"threat\b",
        r"recommendation", r"alert\b", r"blackout", r"radiation",
        r"cme\b", r"sep\b", r"current state",
    ],
}


class Planner:
    """
    Receives a user query + ReasoningContext and produces a Plan.
    """

    def classify_intent(self, query: str) -> str:
        """Classify the user's intent based on keyword patterns."""
        query_lower = query.lower().strip()

        # Slash command shortcuts
        if query_lower.startswith("/explain"):
            return "explain"
        if query_lower.startswith("/compare"):
            return "compare"
        if query_lower.startswith("/report"):
            return "report"
        if query_lower.startswith("/literature"):
            return "literature"

        scores: Dict[str, int] = {intent: 0 for intent in INTENT_PATTERNS}
        for intent, patterns in INTENT_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    scores[intent] += 1

        best = max(scores, key=scores.get)  # type: ignore
        if scores[best] == 0:
            return "general"
        return best

    def create_plan(self, query: str, context: Any) -> Plan:
        """Decompose a query into an ordered list of subtasks."""
        intent = self.classify_intent(query)
        logger.info(f"Classified intent: '{intent}' for query: '{query[:80]}...'")

        subtasks: List[SubTask] = []

        if intent == "explain":
            subtasks = [
                SubTask(agent="physics", action="analyze", params={"query": query}),
                SubTask(agent="spectral", action="analyze", params={"query": query}),
                SubTask(agent="prediction", action="get_context", params={}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "Physics & Spectral analysis with prediction context"

        elif intent == "predict":
            subtasks = [
                SubTask(agent="prediction", action="forecast", params={"query": query}),
                SubTask(agent="physics", action="get_summary", params={}),
                SubTask(agent="mission", action="get_risk", params={}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "Prediction analysis with physics and mission risk context"

        elif intent == "compare":
            subtasks = [
                SubTask(agent="knowledge_graph", action="search", params={"query": query}),
                SubTask(agent="digital_twin", action="similarity", params={"query": query}),
                SubTask(agent="physics", action="get_summary", params={}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "Historical comparison via Knowledge Graph and Digital Twin"

        elif intent == "report":
            subtasks = [
                SubTask(agent="mission", action="get_status", params={}),
                SubTask(agent="physics", action="get_summary", params={}),
                SubTask(agent="prediction", action="forecast", params={}),
                SubTask(agent="digital_twin", action="get_state", params={}),
                SubTask(agent="knowledge_graph", action="get_summary", params={}),
                SubTask(agent="report", action="generate", params={"query": query}),
            ]
            summary = "Full mission report generation"

        elif intent == "literature":
            subtasks = [
                SubTask(agent="literature", action="search", params={"query": query}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "Literature search and review"

        elif intent == "experiment":
            subtasks = [
                SubTask(agent="experiment", action="query", params={"query": query}),
                SubTask(agent="prediction", action="get_context", params={}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "Experiment and benchmark analysis"

        elif intent == "mission":
            subtasks = [
                SubTask(agent="mission", action="get_status", params={}),
                SubTask(agent="mission", action="get_risk", params={}),
                SubTask(agent="prediction", action="forecast", params={}),
                SubTask(agent="digital_twin", action="get_state", params={}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "Full mission status briefing"

        else:  # general
            subtasks = [
                SubTask(agent="mission", action="get_status", params={}),
                SubTask(agent="physics", action="get_summary", params={}),
                SubTask(agent="prediction", action="get_context", params={}),
                SubTask(agent="review", action="validate", params={}),
            ]
            summary = "General multi-agent synthesis"

        plan = Plan(intent=intent, subtasks=subtasks, summary=summary)
        logger.info(f"Plan created: {len(subtasks)} subtasks — {summary}")
        return plan
