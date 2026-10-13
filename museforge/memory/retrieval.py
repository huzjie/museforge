"""Proactive retrieval: top-k relevant memories under a token budget."""
from __future__ import annotations

import time
from typing import List, Tuple

from .store import MemoryStore
from .scoring import MemoryScorer
from .encoder import Encoder
from ..utils.text import tokenize


class Retriever:
    def __init__(self, cfg, encoder: Encoder = None, scorer: MemoryScorer = None):
        self.cfg = cfg
        self.encoder = encoder or Encoder(cfg.embed_dim)
        self.scorer = scorer or MemoryScorer(cfg)

    def retrieve(self, query: str, store: MemoryStore, k: int = None,
                 budget: int = None) -> List[Tuple]:
        """Return [(memory, score), ...] ranked by score, capped by k and budget.

        Marking accessed memories bumps their frequency weight on the next turn.
        """
        k = k if k is not None else self.cfg.top_k
        budget = budget if budget is not None else self.cfg.token_budget
        q_embed = self.encoder.encode(query)
        now = time.time()
        scored = []
        for m in store.all():
            s = self.scorer.score(m, q_embed, now)
            scored.append((m, s))
        scored.sort(key=lambda t: t[1], reverse=True)
        picked: List[Tuple] = []
        used = 0
        for m, s in scored:
            if len(picked) >= k:
                break
            cost = len(tokenize(m.content)) or 1
            if budget > 0 and used + cost > budget:
                continue
            m.access_count += 1
            picked.append((m, s))
            used += cost
        return picked
