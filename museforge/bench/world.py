"""Deterministic ground-truth used by both benchmarks.

Every query / goal / candidate is keyed by a stable seed, so the exact same
candidate set and correct answer are reproduced on every run. This is what
makes the skill -> metric curves clean and reproducible.
"""
from __future__ import annotations

from ..utils.hash import stable_hash, stable_float

GOAL_VOCAB = [
    "complete the regional project review report",
    "migrate the dashboard from MySQL to PostgreSQL",
    "onboard a new agent skill for document generation",
    "stand up a project monitoring room",
    "deliver a training deck on value-driven delivery",
    "unify data sources across institutions",
]


def make_memory_query(i: int) -> str:
    return "query-%04d" % i


def make_memory_candidates(query: str, n_candidates: int = 10):
    """Return a list of candidate dicts with exactly one `is_correct=True`."""
    h = stable_hash(query)
    correct_idx = h % n_candidates
    out = []
    for j in range(n_candidates):
        out.append({
            "id": "%s-cand-%d" % (query, j),
            "content": "candidate %d for %s" % (j, query),
            "is_correct": (j == correct_idx),
        })
    return out


def make_goal(seed: int, n_subgoals: int = 6):
    h = stable_hash("goal-%d" % seed)
    goal_id = "goal-%08x" % (h & 0xFFFFFFFF)
    description = GOAL_VOCAB[h % len(GOAL_VOCAB)]
    subgoal_ids = ["%s-sg-%d" % (goal_id, i) for i in range(n_subgoals)]
    return goal_id, description, subgoal_ids
