"""Deterministic, fast hashing primitives (no numpy / no hash()).

`hash()` is salted per-process in CPython, so it cannot be used to produce
reproducible "embeddings". We use md5 instead: it is fast and the first 8 bytes
give plenty of entropy for seeding `random.Random`.
"""
import hashlib


def stable_hash(key: str) -> int:
    """Return a stable 64-bit integer for a string key."""
    if not isinstance(key, str):
        key = str(key)
    return int.from_bytes(hashlib.md5(key.encode("utf-8")).digest()[:8], "big")


def stable_float(key: str, lo: float = 0.0, hi: float = 1.0) -> float:
    """Return a deterministic float in [lo, hi) for a string key."""
    h = stable_hash(key)
    return lo + (hi - lo) * (h / float(2 ** 64))
