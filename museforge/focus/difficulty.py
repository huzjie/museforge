"""Difficulty / obstacle detection: is the agent stuck?"""
from __future__ import annotations

import time

from .goal import Goal


class DifficultyDetector:
    def __init__(self, cfg):
        self.cfg = cfg

    def steps_since_progress(self, goal: Goal, now: float = None) -> int:
        now = now if now is not None else time.time()
        return goal.attempts

    def is_stuck(self, goal: Goal) -> bool:
        """Stuck = no progress for `staleness_threshold` attempts."""
        if goal.is_done():
            return False
        return goal.attempts >= self.cfg.staleness_threshold and goal.failures > 0

    def failure_rate(self, goal: Goal) -> float:
        if goal.attempts == 0:
            return 0.0
        return goal.failures / goal.attempts

    def difficulty(self, goal: Goal) -> float:
        """0..1 difficulty estimate from the observed failure rate."""
        return min(1.0, self.failure_rate(goal))
