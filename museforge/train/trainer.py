"""Trainer for the mock backend.

The training signal is deliberately simple and monotonic: each step nudges
`skill` upward (0.5 -> 1.0). Memory precision and focus persistence both rise
monotonically with skill, which is what the benchmarks assert.
"""
from __future__ import annotations


class Trainer:
    def __init__(self, backend, cfg=None):
        self.backend = backend
        self.cfg = cfg

    def train(self, steps: int = 10, delta: float = 0.05) -> list:
        """Run `steps` training steps; return the skill trajectory."""
        traj = [getattr(self.backend, "skill", 1.0)]
        for _ in range(steps):
            fn = getattr(self.backend, "train_step", None)
            if fn is None:
                traj.append(traj[-1])
                continue
            fn(delta)
            traj.append(getattr(self.backend, "skill", 1.0))
        return traj
