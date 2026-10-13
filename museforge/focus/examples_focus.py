"""Small demo of the Active Focus subsystem (standalone, no server)."""
from museforge.config import load_config
from museforge.focus import FocusManager


def main():
    cfg = load_config()
    fm = FocusManager(cfg.focus)

    goal = fm.new_goal("完成区域项目巡检报告的自动生成")
    print("Goal:", goal.description)
    print("Subgoals:", goal.subgoals)

    # simulate attempts with occasional failures
    outcomes = [True, False, True, True]
    for ok in outcomes:
        st = fm.step(goal, ok)
        print("  step ->", st)

    print("Focus score:", round(fm.focus_score(goal), 3))


if __name__ == "__main__":
    main()
