# API

## Python

    from museforge import MuseAgent, Config
    agent = MuseAgent(Config())
    agent.remember("user prefers bullets", kind="semantic", importance=0.9)
    out = agent.respond("帮我写周报")
    # out["response"], out["retrieved"]

    agent.set_goal("完成区域巡检报告自动生成")
    agent.step(True)          # 记录一次子目标尝试结果
    agent.focus.focus_score(agent.goal)

## HTTP（`python -m museforge.cli serve`）

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| GET | `/v1/models` | 列出后端 |
| POST | `/v1/chat/completions` | OpenAI 兼容对话（记忆增强） |
| POST | `/v1/memories` | 写入记忆 `{content, kind, importance}` |
| GET | `/v1/memories` | 列出记忆 |
| POST | `/v1/retrieve` | 检索 `{query, k}` |
| POST | `/v1/goal` | 设目标 `{description}` |
| GET | `/v1/focus` | 当前专注状态 |

## CLI

    python -m museforge.cli doctor
    python -m museforge.cli demo "帮我写周报"
    python -m museforge.cli bench --steps 10
    python -m museforge.cli train --steps 10
    python -m museforge.cli serve
