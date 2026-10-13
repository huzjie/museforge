"""Alternative path exploration: when stuck, generate alternative decompositions."""
from __future__ import annotations

from .goal import Goal
from ..utils.hash import stable_hash


class Explorer:
    def __init__(self, cfg):
        self.cfg = cfg

    def alternatives(self, goal: Goal) -> list:
        """Deterministic alternative action plans for a stuck goal."""
        h = stable_hash(goal.description)
        n = min(self.cfg.max_alternatives, max(1, len(goal.subgoals)))
        out = []
        for i in range(n):
            seed = h + i * 0x9E3779B97F4A7C15
            out.append("alt-path %d: reframe '%s' via strategy #%d" % (i + 1, goal.description[:24], seed % 1000))
        return out

    def reframe(self, goal: Goal) -> str:
        """A single reframed objective used to break out of a local dead-end."""
        return "reframed: %s (with a simpler intermediate target)" % goal.description
