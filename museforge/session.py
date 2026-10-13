"""Session management: isolate per-conversation context across turns."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Session:
    id: str
    created_at: float = field(default_factory=time.time)
    last_active: float = field(default_factory=time.time)
    turns: List[Dict] = field(default_factory=list)
    metadata: Dict = field(default_factory=dict)

    def record(self, role: str, content: str):
        self.turns.append({"role": role, "content": content, "ts": time.time()})
        self.last_active = time.time()

    def age(self, now: float = None) -> float:
        now = now if now is not None else time.time()
        return max(0.0, now - self.last_active)


class SessionManager:
    def __init__(self, ttl: float = 3600.0):
        self.ttl = ttl
        self._sessions: Dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        if session_id not in self._sessions:
            self._sessions[session_id] = Session(id=session_id)
        return self._sessions[session_id]

    def close(self, session_id: str):
        self._sessions.pop(session_id, None)

    def expire(self, now: float = None):
        now = now if now is not None else time.time()
        stale = [sid for sid, s in self._sessions.items() if s.age(now) > self.ttl]
        for sid in stale:
            self._sessions.pop(sid, None)
        return len(stale)

    def __len__(self) -> int:
        return len(self._sessions)
