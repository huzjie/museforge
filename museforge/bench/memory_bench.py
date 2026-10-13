"""Memory benchmark: recall@1 / recall@5 / MRR as a function of skill."""
from __future__ import annotations

from .world import make_memory_query, make_memory_candidates


def run_recall(backend, n_queries: int = 50, n_candidates: int = 10, k: int = 5):
    recall_at_1 = 0.0
    recall_at_k = 0.0
    mrr = 0.0
    for i in range(n_queries):
        q = make_memory_query(i)
        cands = make_memory_candidates(q, n_candidates)
        ranked = backend.rank_memories(q, cands)
        correct_idx = next(j for j, c in enumerate(ranked) if c.get("is_correct"))
        if correct_idx == 0:
            recall_at_1 += 1.0
        if correct_idx < k:
            recall_at_k += 1.0
        mrr += 1.0 / (correct_idx + 1)
    return {
        "n_queries": n_queries,
        "n_candidates": n_candidates,
        "recall@1": recall_at_1 / n_queries,
        "recall@%d" % k: recall_at_k / n_queries,
        "mrr": mrr / n_queries,
    }
