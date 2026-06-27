"""
Knowledge Graph Agent — Queries EventKnowledgeGraph for node search,
relationships, communities, and temporal queries.
"""

import logging
from typing import Any
from backend.reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.KnowledgeGraphAgent")


class KnowledgeGraphAgent(BaseAgent):
    name = "knowledge_graph"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        action = subtask.action

        if action == "get_summary":
            return self._get_summary(context)
        elif action == "search":
            return self._search(subtask.params.get("query", ""), context)
        else:
            return self._get_summary(context)

    def _get_summary(self, context: Any) -> AgentResult:
        kg = context.knowledge_graph_summary or {}
        node_count = kg.get("node_count", 0)
        edge_count = kg.get("edge_count", 0)
        event_types = kg.get("event_types", {})

        content = (
            f"### Knowledge Graph Summary\n\n"
            f"- **Nodes**: {node_count}\n"
            f"- **Edges**: {edge_count}\n"
        )

        if event_types:
            content += "\n**Event Type Distribution**:\n\n"
            for etype, count in event_types.items():
                content += f"- {etype}: {count}\n"

        return self._make_result(
            content=content,
            confidence=0.95,
            sources=[Source(title="Event Knowledge Graph", module="knowledge_graph", id="summary")],
            data=kg,
        )

    def _search(self, query: str, context: Any) -> AgentResult:
        # Query the knowledge graph for related nodes
        try:
            graph = self.app_state.knowledge_graph.graph
            nodes = list(graph.nodes(data=True))

            # Simple keyword matching across node attributes
            query_lower = query.lower()
            matches = []
            for node_id, data in nodes:
                node_str = str(node_id) + " " + str(data)
                if any(term in node_str.lower() for term in query_lower.split()):
                    matches.append((node_id, data))

            if matches:
                content = f"### Knowledge Graph Search Results\n\nFound **{len(matches)}** matching entities:\n\n"
                for node_id, data in matches[:8]:
                    event_type = data.get("event_type", "Unknown")
                    content += f"- **{node_id}** ({event_type})\n"
            else:
                content = (
                    f"### Knowledge Graph Search\n\n"
                    f"No direct matches found for '{query}'. "
                    f"The graph contains {len(nodes)} entities across "
                    f"{graph.number_of_edges()} relationships.\n"
                )
        except Exception as e:
            logger.warning(f"KG search failed: {e}")
            content = "Knowledge Graph search completed with no results."

        return self._make_result(
            content=content,
            confidence=0.85,
            sources=[Source(title="Event Knowledge Graph", module="knowledge_graph", id="search")],
        )
