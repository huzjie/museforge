"""Aggregate and format benchmark results."""
from __future__ import annotations


def summarize(memory: dict, focus: dict) -> dict:
    return {"memory": memory, "focus": focus}


def format_report(result: dict) -> str:
    lines = ["Benchmark summary", "=" * 40]
    mem = result.get("memory", {})
    if mem:
        lines.append("[Memory] recall@1=%.3f recall@5=%.3f MRR=%.3f" % (
            mem.get("recall@1", 0.0),
            mem.get("recall@5", 0.0),
            mem.get("mrr", 0.0),
        ))
    foc = result.get("focus", {})
    if foc:
        lines.append("[Focus] completion=%.3f progress=%.3f persistence=%.3f" % (
            foc.get("goal_completion_rate", 0.0),
            foc.get("avg_progress", 0.0),
            foc.get("persistence", 0.0),
        ))
    return "\n".join(lines)
