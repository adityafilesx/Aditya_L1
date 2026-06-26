"""
Digital Twin Agent — Queries the Solar Digital Twin for region state,
historical similarity, and 3D solar state.
"""

import logging
import json
from typing import Any
from reasoning.agents.base_agent import BaseAgent, AgentResult, Source

logger = logging.getLogger("SRE.DigitalTwinAgent")


class DigitalTwinAgent(BaseAgent):
    name = "digital_twin"

    def __init__(self, app_state):
        self.app_state = app_state

    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        action = subtask.action

        if action == "get_state":
            return self._get_state(context)
        elif action == "similarity":
            return self._similarity(subtask.params.get("query", ""), context)
        else:
            return self._get_state(context)

    def _get_state(self, context: Any) -> AgentResult:
        twin = context.digital_twin or {}
        regions = context.active_regions or {}

        global_state = twin.get("global_state", {})
        region_count = len(regions) if isinstance(regions, dict) else 0

        content = (
            f"### Solar Digital Twin State\n\n"
            f"- **Active Regions Tracked**: {region_count}\n"
            f"- **Solar Cycle Phase**: {global_state.get('cycle_phase', 'ascending')}\n"
            f"- **Disk Activity Level**: {global_state.get('activity_level', 'moderate')}\n\n"
        )

        if isinstance(regions, dict) and regions:
            content += "| Region | Hale Class | McIntosh | Lat | Lon |\n|---|---|---|---|---|\n"
            for ar_id, ar_data in list(regions.items())[:5]:
                if isinstance(ar_data, dict):
                    content += (
                        f"| {ar_id} "
                        f"| {ar_data.get('hale_class', '—')} "
                        f"| {ar_data.get('mcintosh_class', '—')} "
                        f"| {ar_data.get('lat', '—')} "
                        f"| {ar_data.get('lon', '—')} |\n"
                    )
            content += "\n"

        if context.selected_region_id:
            content += f"> 📍 Currently tracking **{context.selected_region_id}**.\n"

        return self._make_result(
            content=content,
            confidence=0.95,
            sources=[Source(title="Solar Digital Twin", module="digital_twin", id="state")],
            data={"global_state": global_state, "region_count": region_count},
        )

    def _similarity(self, query: str, context: Any) -> AgentResult:
        # Try to extract an AR number from the query
        import re
        ar_match = re.search(r"AR\s*(\d+)", query, re.IGNORECASE)
        
        if ar_match:
            ar_num = int(ar_match.group(1))
            try:
                sim = self.app_state.digital_twin.find_historical_similarity(ar_num)
                content = (
                    f"### Historical Similarity for AR{ar_num}\n\n"
                    f"The Digital Twin found the following historical matches:\n\n"
                )
                if isinstance(sim, list):
                    for match in sim[:5]:
                        content += f"- **AR{match.get('ar_num', '?')}**: Similarity = {match.get('score', 0):.2f}\n"
                elif isinstance(sim, dict):
                    content += f"```json\n{json.dumps(sim, indent=2)}\n```\n"
                else:
                    content += f"Result: {sim}\n"
                return self._make_result(
                    content=content,
                    confidence=0.88,
                    sources=[Source(title="Digital Twin Similarity Engine", module="digital_twin", id=f"AR{ar_num}")],
                )
            except Exception as e:
                logger.warning(f"Similarity search failed: {e}")

        content = (
            f"### Historical Event Comparison\n\n"
            f"To perform a detailed similarity search, the Digital Twin compares "
            f"magnetic morphology, Hale classification, McIntosh class, and temporal "
            f"evolution patterns against the historical solar cycle archive.\n\n"
            f"Currently {len(context.active_regions) if isinstance(context.active_regions, dict) else 0} "
            f"active regions are being tracked.\n"
        )
        return self._make_result(
            content=content,
            confidence=0.80,
            sources=[Source(title="Digital Twin", module="digital_twin", id="similarity")],
        )
