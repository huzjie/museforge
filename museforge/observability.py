"""Observability: counters/gauges + focus telemetry (zero-dependency)."""
from __future__ import annotations

from collections import defaultdict
from typing import Dict, List


class Metrics:
    def __init__(self):
        self.counters: Dict[str, int] = defaultdict(int)
        self.gauges: Dict[str, float] = {}

    def inc(self, name: str, n: int = 1):
        self.counters[name] += n

    def set(self, name: str, value: float):
        self.gauges[name] = value

    def snapshot(self) -> Dict:
        return {"counters": dict(self.counters), "gauges": dict(self.gauges)}


class FocusTelemetry:
    """Track focus_score over time to catch regressions."""

    def __init__(self, window: int = 100):
        self.window = window
        self.history: List[float] = []

    def record(self, focus_score: float):
        self.history.append(focus_score)
        if len(self.history) > self.window:
            self.history = self.history[-self.window:]

    def recent_mean(self, n: int = 10) -> float:
        if not self.history:
            return 0.0
        tail = self.history[-n:]
        return sum(tail) / len(tail)

    def below(self, threshold: float) -> bool:
        return self.recent_mean() < threshold
