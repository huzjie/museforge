"""Deterministic vector math for memory embeddings (zero-dependency).

We model embeddings with md5-seeded pseudo-random unit vectors. This is a
*reference* implementation: swap in a real sentence-encoder in production via
the encoder interface.
"""
import math
import random

from .hash import stable_hash


def stable_vector(key: str, dim: int = 64) -> list:
    """Deterministic pseudo-random vector of length `dim`, roughly uniform in [-1, 1]."""
    rng = random.Random(stable_hash(key))
    return [rng.uniform(-1.0, 1.0) for _ in range(dim)]


def dot(a: list, b: list) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: list) -> float:
    s = math.sqrt(sum(x * x for x in a))
    return s if s > 0 else 1.0


def cosine(a: list, b: list) -> float:
    return dot(a, b) / (norm(a) * norm(b))


def normalize(a: list) -> list:
    n = norm(a)
    return [x / n for x in a]
