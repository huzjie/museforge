"""Memory eviction policies: LRU / LFU / FIFO."""
from __future__ import annotations

from typing import List

from .types import Memory


def evict_lru(memories: List[Memory], keep: int) -> List[Memory]:
    """Keep the most recently accessed; evict the rest (LRU by created_at as fallback)."""
    ranked = sorted(memories, key=lambda m: (m.access_count, m.created_at), reverse=True)
    return ranked[:keep]


def evict_lfu(memories: List[Memory], keep: int) -> List[Memory]:
    """Keep the least frequently accessed first (ascending access_count)."""
    ranked = sorted(memories, key=lambda m: m.access_count)
    return ranked[:keep]


def evict_fifo(memories: List[Memory], keep: int) -> List[Memory]:
    """Keep the oldest (FIFO order); evict newest beyond `keep`."""
    ranked = sorted(memories, key=lambda m: m.created_at)
    return ranked[:keep]
