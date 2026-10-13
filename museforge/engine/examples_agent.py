"""End-to-end demo: memory + focus + generation in one agent loop."""
from museforge import MuseAgent, Config


def main():
    agent = MuseAgent(Config())

    # seed durable memories
    agent.remember("User prefers concise, bullet-style answers.", kind="semantic", importance=0.9)
    agent.remember("User is building a PMO project-monitoring dashboard.", kind="semantic", importance=0.8)
    agent.remember("User's team covers Shanghai, Zhejiang, Shandong.", kind="semantic", importance=0.7)

    out = agent.respond("帮我写周报")
    print("Q:", out["query"])
    print("A:", out["response"])
    print("Retrieved:")
    for content, score in out["retrieved"]:
        print("   [%.3f] %s" % (score, content[:60]))

    # focus demo
    agent.set_goal("完成区域巡检报告自动生成")
    for ok in [True, False, True, True]:
        agent.step(ok)
    print("\nFocus score:", round(agent.focus.focus_score(agent.goal), 3))


if __name__ == "__main__":
    main()
