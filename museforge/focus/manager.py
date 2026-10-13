"""FocusManager: orchestrates goal lifecycle and measures Active Focus quality."""
from __future__ import annotations

import time
from typing import Dict

from .goal import Goal
from .planner import Planner
from .tracker import Tracker
from .difficulty import DifficultyDetector
from .explorer import Explorer
from ..utils.hash import stable_hash


class FocusManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.planner = Planner(cfg)
        self.tracker = Tracker(cfg)
        self.detector = DifficultyDetector(cfg)
        self.explorer = Explorer(cfg)

    def new_goal(self, description: str) -> Goal:
        sub = self.planner.decompose(description)
        return Goal(
            id="goal-%08x" % (stable_hash(description + str(time.time())) & 0xFFFFFFFF),
            description=description,
            subgoals=sub,
            completed=[False] * len(sub),
        )

    def step(self, goal: Goal, success: bool) -> Dict:
        """Record one subgoal attempt and return the resulting focus state."""
        goal.attempts += 1
        idx = goal.current_index()
        if success:
            if idx >= 0:
                goal.completed[idx] = True
                goal.last_progress_at = time.time()
        else:
            goal.failures += 1

        return self.state(goal)

    def state(self, goal: Goal) -> Dict:
        stuck = self.detector.is_stuck(goal)
        return {
            "progress": goal.progress(),
            "is_done": goal.is_done(),
            "is_stuck": stuck,
            "difficulty": self.detector.difficulty(goal),
            "attempts": goal.attempts,
            "failures": goal.failures,
            "alternatives": self.explorer.alternatives(goal) if stuck else [],
        }

    def focus_score(self, goal: Goal) -> float:
        """Composite Active Focus quality in [0, 1].

        = 0.5 * progress + 0.3 * persistence + 0.2 * adaptivity

        * persistence: 1 - difficulty (the agent keeps pushing instead of giving up)
        * adaptivity:  whether alternative paths were explored when stuck
        """
        progress = goal.progress()
        persistence = 1.0 - self.detector.difficulty(goal)
        adaptivity = 1.0 if goal.alternates_tried > 0 or not self.detector.is_stuck(goal) else 0.0
        if goal.is_done():
            adaptivity = 1.0
        return 0.5 * progress + 0.3 * persistence + 0.2 * adaptivity
