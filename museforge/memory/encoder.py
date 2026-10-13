"""Memory encoder: text -> deterministic vector.

The reference encoder uses md5-seeded pseudo-random unit vectors so the whole
pipeline runs with zero dependencies. Swap in a real embedding model by
subclassing and overriding :meth:`encode`.
"""
from __future__ import annotations

from ..utils.vectors import stable_vector


class Encoder:
    def __init__(self, dim: int = 64):
        self.dim = dim

    def encode(self, text: str) -> list:
        if not text:
            return [0.0] * self.dim
        return stable_vector(text, self.dim)
