"""
Research Memory — In-memory conversation store with links to platform entities.
"""

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

logger = logging.getLogger("SRE.Memory")


@dataclass
class MemoryMessage:
    role: str  # "user" or "ai"
    content: str
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ResearchSession:
    session_id: str
    title: str
    messages: List[MemoryMessage] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    # Links to platform entities
    linked_region_ids: List[str] = field(default_factory=list)
    linked_graph_node_ids: List[str] = field(default_factory=list)
    linked_experiment_ids: List[str] = field(default_factory=list)
    linked_timeline_snapshots: List[float] = field(default_factory=list)


class ResearchMemory:
    """In-memory research session store."""

    def __init__(self):
        self.sessions: Dict[str, ResearchSession] = {}
        self._default_session_id = "default"
        # Create a default session
        self.sessions[self._default_session_id] = ResearchSession(
            session_id=self._default_session_id,
            title="Default Research Session",
        )

    def get_or_create_session(self, session_id: Optional[str] = None) -> ResearchSession:
        sid = session_id or self._default_session_id
        if sid not in self.sessions:
            self.sessions[sid] = ResearchSession(
                session_id=sid,
                title=f"Research Session {len(self.sessions) + 1}",
            )
        return self.sessions[sid]

    def add_message(
        self,
        role: str,
        content: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        session = self.get_or_create_session(session_id)
        msg = MemoryMessage(role=role, content=content, metadata=metadata or {})
        session.messages.append(msg)
        logger.info(f"Memory: added {role} message to session '{session.session_id}'")

    def get_history(self, session_id: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]:
        session = self.get_or_create_session(session_id)
        return [
            {
                "role": m.role,
                "content": m.content,
                "timestamp": m.timestamp,
                "metadata": m.metadata,
            }
            for m in session.messages[-limit:]
        ]

    def list_sessions(self) -> List[Dict[str, Any]]:
        return [
            {
                "session_id": s.session_id,
                "title": s.title,
                "message_count": len(s.messages),
                "created_at": s.created_at,
            }
            for s in self.sessions.values()
        ]
