"""Memory data model: episodic vs semantic memories."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

EPISODIC = "episodic"
SEMANTIC = "semantic"


@dataclass
class Memory:
    """A single unit of remembered context.

    * episodic: a concrete past interaction / event ("the user asked for X on Tue").
    * semantic: a distilled, durable fact or preference ("the user prefers Y").
    """

    id: str
    kind: str
    content: str
    source: str = "user"
    created_at: float = field(default_factory=time.time)
    importance: float = 0.5
    access_count: int = 0
    embed: List[float] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "content": self.content,
            "source": self.source,
            "created_at": self.created_at,
            "importance": self.importance,
            "access_count": self.access_count,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Memory":
        return cls(
            id=d["id"],
            kind=d.get("kind", EPISODIC),
            content=d.get("content", ""),
            source=d.get("source", "user"),
            created_at=d.get("created_at", time.time()),
            importance=d.get("importance", 0.5),
            access_count=d.get("access_count", 0),
        )

    def age(self, now: Optional[float] = None) -> float:
        now = now if now is not None else time.time()
        return max(0.0, now - self.created_at)
