"""Goal decomposition: break a hard goal into ordered subgoals (deterministic)."""
from __future__ import annotations

from ..utils.hash import stable_hash

VERBS = ["define", "collect", "design", "implement", "verify", "review", "deploy", "document"]


class Planner:
    def __init__(self, cfg):
        self.cfg = cfg

    def decompose(self, description: str) -> list:
        """Deterministic decomposition keyed by the goal description."""
        h = stable_hash(description)
        span = max(1, self.cfg.max_subgoals - 2)
        n = 3 + (h % span)
        out = []
        for i in range(n):
            verb = VERBS[(h >> (i * 3)) % len(VERBS)]
            out.append("%s %s (subgoal %d)" % (verb, description[:28], i + 1))
        return out
