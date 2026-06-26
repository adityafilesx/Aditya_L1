"""
Base Agent — Abstract interface for all specialized reasoning agents.

Every agent receives a SubTask + ReasoningContext and returns an AgentResult.
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("SRE.Agent")


@dataclass
class Source:
    """A traceable source that an agent used to form its conclusion."""
    title: str
    module: str  # e.g. "physics_engine", "digital_twin", "knowledge_graph"
    id: str = ""
    url: str = ""


@dataclass
class AgentResult:
    """Structured output from a specialized agent."""
    agent_name: str
    content: str  # Markdown-formatted reasoning output
    confidence: float = 0.0  # 0.0 to 1.0
    sources: List[Source] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)  # Raw structured data
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent": self.agent_name,
            "content": self.content,
            "confidence": self.confidence,
            "sources": [{"title": s.title, "module": s.module, "id": s.id} for s in self.sources],
            "data": self.data,
            "warnings": self.warnings,
        }


class BaseAgent(ABC):
    """Abstract base class for all specialized agents."""

    name: str = "base"

    @abstractmethod
    async def execute(self, subtask: Any, context: Any) -> AgentResult:
        """Execute a subtask given the current reasoning context."""
        ...

    def _make_result(
        self,
        content: str,
        confidence: float = 0.85,
        sources: Optional[List[Source]] = None,
        data: Optional[Dict[str, Any]] = None,
        warnings: Optional[List[str]] = None,
    ) -> AgentResult:
        return AgentResult(
            agent_name=self.name,
            content=content,
            confidence=confidence,
            sources=sources or [],
            data=data or {},
            warnings=warnings or [],
        )
