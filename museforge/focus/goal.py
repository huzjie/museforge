"""Goal data model: description, subgoals, progress, attempts."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import List


@dataclass
class Goal:
    id: str
    description: str
    subgoals: List[str] = field(default_factory=list)
    completed: List[bool] = field(default_factory=list)
    attempts: int = 0
    failures: int = 0
    alternates_tried: int = 0
    created_at: float = field(default_factory=time.time)
    last_progress_at: float = field(default_factory=time.time)

    def progress(self) -> float:
        if not self.subgoals:
            return 0.0
        return sum(1 for c in self.completed if c) / len(self.subgoals)

    def is_done(self) -> bool:
        return bool(self.subgoals) and all(self.completed)

    def current_index(self) -> int:
        """Index of the first uncompleted subgoal (or -1 if done)."""
        for i, c in enumerate(self.completed):
            if not c:
                return i
        return -1
