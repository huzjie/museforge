"""Progress tracking for goals."""
from __future__ import annotations

from .goal import Goal


class Tracker:
    def __init__(self, cfg):
        self.cfg = cfg

    def progress(self, goal: Goal) -> float:
        return goal.progress()

    def done_count(self, goal: Goal) -> int:
        return sum(1 for c in goal.completed if c)

    def total_count(self, goal: Goal) -> int:
        return len(goal.subgoals)
