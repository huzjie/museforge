"""End-to-end demo: memory + focus + generation."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from museforge import MuseAgent, Config


def main():
    agent = MuseAgent(Config())

    agent.remember("用户偏好简洁、要点式、能落地的回答", kind="semantic", importance=0.9)
    agent.remember("用户在用友做项目管理，关注区域巡检报告", kind="semantic", importance=0.8)
    agent.remember("用户的团队覆盖上海、浙江、山东", kind="semantic", importance=0.7)

    out = agent.respond("帮我写周报")
    print("Q:", out["query"])
    print("A:", out["response"])
    print("Retrieved:")
    for content, score in out["retrieved"]:
        print("   [%.3f] %s" % (score, content[:70]))

    agent.set_goal("完成区域巡检报告自动生成")
    for ok in [True, False, True, True]:
        agent.step(ok)
    print()
    print("Focus score:", round(agent.focus.focus_score(agent.goal), 3))
    print("Goal state:", agent.focus_state())


if __name__ == "__main__":
    main()
