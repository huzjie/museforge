"""Active Focus standalone demo."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from museforge import Config
from museforge.focus import FocusManager


def main():
    fm = FocusManager(Config().focus)
    goal = fm.new_goal("完成区域巡检报告自动生成")
    print("Subgoals:")
    for i, s in enumerate(goal.subgoals, 1):
        print("  %d. %s" % (i, s))
    print()
    for ok in [True, False, True, True]:
        st = fm.step(goal, ok)
        print("step -> progress=%.2f stuck=%s difficulty=%.2f" % (st["progress"], st["is_stuck"], st["difficulty"]))
    print("Focus score:", round(fm.focus_score(goal), 3))


if __name__ == "__main__":
    main()
