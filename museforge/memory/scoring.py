"""Memory scoring: relevance + recency + importance + frequency.

score(m) = w_rel * relevance + w_rec * recency + w_imp * importance + w_freq * freq

This is the "proactive" part of Active Memory: instead of dumping the whole
history, we rank memories and pull only the top-k under a token budget.
"""
from __future__ import annotations

import math
import time

from .types import Memory
from ..utils.vectors import cosine


class MemoryScorer:
    def __init__(self, cfg):
        self.cfg = cfg

    def relevance(self, query_embed: list, mem: Memory) -> float:
        if not mem.embed or not query_embed:
            return 0.0
        # cosine in [-1,1] -> [0,1]
        return (cosine(query_embed, mem.embed) + 1.0) / 2.0

    def recency(self, mem: Memory, now: float) -> float:
        hl = self.cfg.half_life_hours * 3600.0
        if hl <= 0:
            return 1.0
        return math.exp(-mem.age(now) / hl)

    def frequency(self, mem: Memory) -> float:
        return math.log(1 + mem.access_count) / math.log(1 + max(1, mem.access_count) + 1)

    def score(self, mem: Memory, query_embed: list, now: float = None) -> float:
        now = now if now is not None else time.time()
        rel = self.relevance(query_embed, mem)
        rec = self.recency(mem, now)
        imp = max(0.0, min(1.0, mem.importance))
        freq = self.frequency(mem)
        w = self.cfg
        return (
            w.w_rel * rel
            + w.w_rec * rec
            + w.w_imp * imp
            + w.w_freq * freq
        )
