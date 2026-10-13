"""MuseAgent: the personal-agent action loop.

Every turn:
  1. *Proactive retrieval* -- pull top-k relevant memories under a token budget
     (Active Memory) instead of injecting the whole history.
  2. *Focus upkeep* -- if a goal is active, evaluate progress / stuck-ness and
     offer alternative paths (Active Focus).
  3. *Generate* -- build a memory-augmented prompt and call the backend.
"""
from __future__ import annotations

import time
from typing import Dict, List, Optional

from ..config import Config
from ..memory import MemoryStore, Retriever, Consolidator, Encoder
from ..memory.types import EPISODIC, SEMANTIC
from ..focus import FocusManager, Goal
from ..model.backends import get_backend


class MuseAgent:
    def __init__(self, cfg: Config = None, backend=None):
        self.cfg = cfg or Config()
        self.backend = backend or get_backend(self.cfg.model.name, self.cfg.model)
        self.encoder = Encoder(self.cfg.memory.embed_dim)
        self.store = MemoryStore(self.cfg.memory, self.encoder)
        self.retriever = Retriever(self.cfg.memory, self.encoder)
        self.consolidator = Consolidator(self.cfg.memory)
        self.focus = FocusManager(self.cfg.focus)
        self.goal: Optional[Goal] = None

    # -- memory -----------------------------------------------------------
    def remember(self, content: str, kind: str = EPISODIC, importance: float = 0.5):
        return self.store.add(content, kind=kind, importance=importance)

    def recall(self, query: str, k: int = None) -> List:
        return self.retriever.retrieve(query, self.store, k=k)

    # -- focus ------------------------------------------------------------
    def set_goal(self, description: str) -> Goal:
        self.goal = self.focus.new_goal(description)
        return self.goal

    def step(self, success: bool) -> Dict:
        if self.goal is None:
            return {}
        return self.focus.step(self.goal, success)

    def focus_state(self) -> Dict:
        if self.goal is None:
            return {}
        return self.focus.state(self.goal)

    # -- generation -------------------------------------------------------
    def respond(self, query: str, k: int = None) -> Dict:
        """Generate a memory-augmented response."""
        memories = self.recall(query, k=k)
        context = self._build_context(memories)
        prompt = self._build_prompt(query, context)
        answer = self.backend.generate(prompt, max_tokens=self.cfg.model.max_tokens)
        if self.consolidator.should_consolidate(self.store):
            created = self.consolidator.consolidate(self.store)
        else:
            created = 0
        return {
            "query": query,
            "response": answer,
            "retrieved": [(m.content, round(s, 3)) for m, s in memories],
            "consolidated": created,
        }

    def _build_context(self, memories: List) -> str:
        if not memories:
            return ""
        lines = []
        for m, _s in memories:
            lines.append("- [%s] %s" % (m.kind, m.content))
        return "\n".join(lines)

    def _build_prompt(self, query: str, context: str) -> str:
        goal_hint = ""
        if self.goal is not None and not self.goal.is_done():
            goal_hint = "\nCurrent goal: %s (progress %.0f%%)" % (
                self.goal.description, self.goal.progress() * 100)
        if context:
            return (
                "You are a personal agent with proactive memory.\n"
                "Relevant remembered context:\n%s\n%s\n\nUser query: %s" % (context, goal_hint, query)
            )
        return "You are a personal agent.%s\n\nUser query: %s" % (goal_hint, query)

    def train(self, delta: float = 0.05) -> float:
        """Bump the mock backend's skill (no-op for fixed backends)."""
        fn = getattr(self.backend, "train_step", None)
        if fn:
            return fn(delta)
        return getattr(self.backend, "skill", 1.0)
