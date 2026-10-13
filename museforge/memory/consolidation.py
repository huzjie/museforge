"""Memory consolidation: distill old episodes into durable semantic facts.

Prevents unbounded context growth. When the episodic buffer grows beyond a
threshold, we deterministically summarize old episodes into compact semantic
memories, keeping the most important/recent episodes untouched.
"""
from __future__ import annotations

import time
from typing import List

from .store import MemoryStore
from .types import SEMANTIC
from ..utils.text import summarize_text


class Consolidator:
    def __init__(self, cfg):
        self.cfg = cfg

    def should_consolidate(self, store: MemoryStore) -> bool:
        return len(store.episodic) >= self.cfg.consolidate_after

    def consolidate(self, store: MemoryStore) -> int:
        """Summarize the oldest half of episodic memories into semantic facts.

        Returns the number of new semantic facts created.
        """
        n = len(store.episodic)
        if n == 0:
            return 0
        # keep the newest half; summarize the oldest half
        cut = n // 2
        old = store.episodic[:cut]
        store.episodic = store.episodic[cut:]
        created = 0
        # group into buckets of 5 for a compact, readable summary
        bucket = []
        for m in old:
            bucket.append(m.content)
            if len(bucket) >= 5:
                self._distill(store, bucket)
                bucket = []
                created += 1
        if bucket:
            self._distill(store, bucket)
            created += 1
        return created

    def _distill(self, store: MemoryStore, contents: List[str]):
        summary = summarize_text(" | ".join(contents), max_tokens=40)
        store.add(summary, kind=SEMANTIC, source="consolidation", importance=0.4)
