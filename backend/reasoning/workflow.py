"""
Workflow Engine — Defines reusable multi-step scientific workflows.
Each workflow is a sequence of agent calls with data piping.
"""

import logging
from typing import Any, List
from backend.reasoning.planner import SubTask

logger = logging.getLogger("SRE.Workflow")


# ── Pre-defined Scientific Workflows ──

WORKFLOWS = {
    "flare_analysis": {
        "name": "Flare Analysis Workflow",
        "description": "Complete flare event analysis: physics → spectral → prediction → review",
        "subtasks": [
            SubTask(agent="physics", action="analyze", params={"query": "flare thermal analysis"}),
            SubTask(agent="spectral", action="analyze", params={"query": "spectral fitting"}),
            SubTask(agent="prediction", action="forecast", params={"query": "flare prediction"}),
            SubTask(agent="digital_twin", action="get_state", params={}),
            SubTask(agent="knowledge_graph", action="search", params={"query": "flare events"}),
            SubTask(agent="review", action="validate", params={}),
        ],
    },
    "mission_briefing": {
        "name": "Mission Briefing Workflow",
        "description": "Full mission status briefing for operators",
        "subtasks": [
            SubTask(agent="mission", action="get_status", params={}),
            SubTask(agent="mission", action="get_risk", params={}),
            SubTask(agent="prediction", action="forecast", params={}),
            SubTask(agent="digital_twin", action="get_state", params={}),
            SubTask(agent="report", action="generate", params={"query": "mission briefing"}),
        ],
    },
    "comparative_analysis": {
        "name": "Comparative Analysis Workflow",
        "description": "Compare current event with historical events",
        "subtasks": [
            SubTask(agent="digital_twin", action="similarity", params={"query": "historical comparison"}),
            SubTask(agent="knowledge_graph", action="search", params={"query": "similar events"}),
            SubTask(agent="physics", action="get_summary", params={}),
            SubTask(agent="literature", action="search", params={"query": "similar solar events"}),
            SubTask(agent="review", action="validate", params={}),
        ],
    },
    "research_deep_dive": {
        "name": "Research Deep-Dive Workflow",
        "description": "Deep scientific analysis for research publications",
        "subtasks": [
            SubTask(agent="physics", action="analyze", params={"query": "deep physics analysis"}),
            SubTask(agent="spectral", action="analyze", params={"query": "full spectral analysis"}),
            SubTask(agent="experiment", action="query", params={"query": "model performance"}),
            SubTask(agent="literature", action="search", params={"query": "related research"}),
            SubTask(agent="review", action="validate", params={}),
        ],
    },
}


def get_workflow(name: str) -> dict:
    return WORKFLOWS.get(name, {})


def list_workflows() -> List[dict]:
    return [
        {"name": w["name"], "description": w["description"], "id": wid}
        for wid, w in WORKFLOWS.items()
    ]
