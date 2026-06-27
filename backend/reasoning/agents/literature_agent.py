"""
Literature Agent — Stub with mocked connectors for NASA ADS and arXiv.
Architecture is ready for real API integration in a future phase.
"""

import logging
from typing import Any
from backend.reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.LiteratureAgent")


# Mocked literature database for demonstration
MOCK_PAPERS = [
    {
        "title": "The Neupert Effect: What Can It Tell Us about the Impulsive Phase?",
        "authors": "Dennis, B.R. & Zarro, D.M.",
        "year": 1993,
        "journal": "Solar Physics",
        "doi": "10.1007/BF00733430",
        "relevance": ["neupert", "impulsive", "sxr", "hxr"],
    },
    {
        "title": "Solar Flare Prediction Using Machine Learning: A Review",
        "authors": "Georgoulis, M.K. et al.",
        "year": 2021,
        "journal": "Space Weather",
        "doi": "10.1029/2020SW002713",
        "relevance": ["prediction", "machine learning", "flare", "forecast"],
    },
    {
        "title": "Coronal Mass Ejections and Solar Energetic Particles",
        "authors": "Reames, D.V.",
        "year": 2013,
        "journal": "Space Science Reviews",
        "doi": "10.1007/s11214-012-9945-9",
        "relevance": ["cme", "sep", "energetic particles", "radiation"],
    },
    {
        "title": "Aditya-L1 Mission: An Overview",
        "authors": "Seetha, S. & Megala, S.",
        "year": 2017,
        "journal": "Current Science",
        "doi": "10.18520/cs/v113/i04/610-615",
        "relevance": ["aditya", "l1", "mission", "solexs", "helios"],
    },
    {
        "title": "Emission Measure Distribution in Solar Active Regions",
        "authors": "Warren, H.P. et al.",
        "year": 2012,
        "journal": "The Astrophysical Journal",
        "doi": "10.1088/0004-637X/759/2/141",
        "relevance": ["emission measure", "temperature", "active region", "dem"],
    },
]


class LiteratureAgent(BaseAgent):
    name = "literature"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        query = subtask.params.get("query", "")
        return self._search(query)

    def _search(self, query: str) -> AgentResult:
        query_lower = query.lower()
        matches = []

        for paper in MOCK_PAPERS:
            score = sum(1 for kw in paper["relevance"] if kw in query_lower)
            if score > 0:
                matches.append((score, paper))

        matches.sort(key=lambda x: x[0], reverse=True)

        if matches:
            content = f"### Literature Search Results\n\nFound **{len(matches)}** relevant publications:\n\n"
            for _, paper in matches:
                content += (
                    f"📄 **{paper['title']}**\n"
                    f"   {paper['authors']} ({paper['year']}) — *{paper['journal']}*\n"
                    f"   DOI: `{paper['doi']}`\n\n"
                )
            content += (
                "\n> ℹ️ *Literature results are from a curated local library. "
                "NASA ADS and arXiv connectors are architecturally prepared but not yet active.*\n"
            )
        else:
            content = (
                f"### Literature Search\n\n"
                f"No direct matches found in the local library for '{query}'. "
                f"Future integration with NASA ADS and arXiv will expand coverage.\n"
            )

        return self._make_result(
            content=content,
            confidence=0.70 if matches else 0.30,
            sources=[Source(title="Local Paper Library", module="literature", id="local")],
            warnings=["Literature results are from a mocked local library"] if not matches else [],
        )
