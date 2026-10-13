"""Focus benchmark: goal completion + persistence as a function of skill."""
from __future__ import annotations

from .world import make_goal


def run_single_goal(backend, goal_id, subgoal_ids, budget: int = 30):
    n = len(subgoal_ids)
    completed = 0
    attempts = 0
    gave_up = False
    idx = 0
    while idx < n and attempts < budget:
        ok = backend.try_subgoal(goal_id, subgoal_ids[idx])
        attempts += 1
        if ok:
            completed += 1
            idx += 1
        else:
            if not backend.persist_after_failure(goal_id, subgoal_ids[idx]):
                gave_up = True
                break
    return {
        "progress": completed / n if n else 0.0,
        "completed": completed,
        "total": n,
        "gave_up": gave_up,
        "attempts": attempts,
    }


def run_focus(backend, n_goals: int = 30, n_subgoals: int = 6, budget: int = 30):
    completion = 0.0
    progress = 0.0
    give_ups = 0.0
    for s in range(n_goals):
        goal_id, _desc, sub_ids = make_goal(s, n_subgoals)
        r = run_single_goal(backend, goal_id, sub_ids, budget)
        progress += r["progress"]
        if r["completed"] == r["total"]:
            completion += 1.0
        if r["gave_up"]:
            give_ups += 1.0
    return {
        "n_goals": n_goals,
        "goal_completion_rate": completion / n_goals,
        "avg_progress": progress / n_goals,
        "give_up_rate": give_ups / n_goals,
        "persistence": 1.0 - give_ups / n_goals,
    }
