# museforge

> 个人智能体的「主动记忆 + 主动专注」引擎 —— Meta Muse Wonder 方向的一个零依赖可运行参考实现。

[![CI](https://github.com/huzjie/museforge/actions/workflows/ci.yml/badge.svg)](https://github.com/huzjie/museforge)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-Apache--2.0-green)
![Zero deps](https://img.shields.io/badge/deps-zero-brightgreen)

---

## 这是什么

Meta 的 Muse Wonder 把个人智能体的两大能力推到了 API 层：**Active Memory（主动记忆）** 和
**Active Focus（主动专注）**。这个仓库不写新闻综述，只做一件事：**把这两个机制拆成可以照做的
工程实现**——思路、打分公式、提示词模板、训练信号，全部给全，`git clone` 下来就能跑。

- **Active Memory**：跨会话记住用户的关键上下文（事实/偏好/决定），每个回合**主动**只检索与
  当前查询相关的那部分（top-k + token 预算），而不是把整段历史塞进 prompt。
- **Active Focus**：一个可测的标量，衡量智能体能否围绕硬目标持续推进、卡住时尝试替代路径、
  适应新信息，而不是轻易放弃。

## 技术原理拆解

### 1. 主动记忆 = 编码 + 四信号打分 + 预算内检索 + 巩固

```
score(m) = w_rel·relevance + w_rec·recency + w_imp·importance + w_freq·freq

relevance = (cosine(q_emb, m_emb) + 1) / 2      # 相关性
recency   = exp(-age / half_life)               # 新近度（半衰期衰减）
freq      = log(1 + access_count) / (log(1 + access_count) + 1)  # 频次
```

关键工程点：
- **检索即复用**：被取中的记忆 `access_count += 1`，下一轮频次权重上升，形成「越常用越靠前」。
- **参考嵌入用 md5 种子伪随机向量**：零依赖、可复现、可回归；生产只需替换 `Encoder.encode`。
- **巩固**：episodic 缓冲超阈值时，把最旧一半蒸馏成 compact 的 semantic 事实，控制上下文增长。

### 2. 主动专注 = 分解 + 追踪 + 卡点检测 + 替代探索

```
focus = 0.5·progress + 0.3·persistence + 0.2·adaptivity
persistence = 1 - difficulty        # difficulty = failures / attempts
```

关键工程点：
- **卡点检测用「连续无进展」计数**（`staleness_threshold` 次），比单次失败更鲁棒。
- **替代路径确定性生成**（目标文本 md5 键控），可在基准里复现、在真实系统里审计。
- **坚持/放弃做成布尔决策** `persist_after_failure`，而不是模糊的「意志力」描述。

### 3. 训练信号：单调趋 1，不是「对+1 错-1」

```
score_memory = (skill-0.5)·2·is_correct + noise    (noise ∈ [0,1))
try_subgoal  = skill >= threshold                  (threshold ∈ [0,1))
```

用「对 +1 / 错 -1」在 skill 低（正确率 <50%）时期望漂移为负，skill 会被压到 0；**恒正 delta**
让 skill 单调爬向 1.0，记忆召回率与目标完成率随之单调上升。详见 `docs/training.md`。

## 可复用的干货块

### 提示词模板（记忆检索意图改写）

```
你是记忆检索意图识别器。给定用户输入，输出 1-3 个用于检索长时记忆的关键短语，
按相关度降序，用 JSON 数组返回。只输出短语本身，不解释。

用户输入：{query}
```

完整模板在 `prompts/`（检索 / 目标分解 / 卡点处理 / 巩固 / 系统设定）。

### 配置片段（`configs/default.yaml`）

```yaml
memory:
  token_budget: 2048
  top_k: 8
  half_life_hours: 24.0
  w_rel: 0.5
  w_rec: 0.2
  w_imp: 0.2
  w_freq: 0.1
  consolidate_after: 200
focus:
  max_subgoals: 8
  staleness_threshold: 3
  persistence_budget: 10
```

### 三条踩坑经验

1. **别把「全量历史」当记忆**——按相关度 top-k 检索才是主动记忆的核心，全量注入必然上下文爆炸。
2. **打分要四信号加权**，纯余弦相似度在语义接近时会召回一堆噪声。
3. **mock 的 boost 在 skill=0.5 时应恰为 0、noise 取 [0,1)**：若 boost 恒 0.5（`skill·is_correct`），
   skill=0.5 时正确项就稳进 top，recall@1 直接 ~0.6，曲线起点过高、失去区分度。

## 快速开始

```bash
# 零依赖，直接跑
python -m museforge.cli doctor        # 自检所有后端/组件
python -m museforge.cli demo "帮我写周报"   # 一次记忆增强问答
python -m museforge.cli bench          # 记忆召回 + 专注坚持度基准
python -m museforge.cli serve          # 起 OpenAI 兼容 HTTP 服务
```

```python
from museforge import MuseAgent, Config

agent = MuseAgent(Config())
agent.remember("用户偏好简洁的要点式回答", kind="semantic", importance=0.9)
out = agent.respond("帮我写周报")
print(out["response"])

agent.set_goal("完成区域巡检报告自动生成")
agent.step(True)
print(agent.focus.focus_score(agent.goal))
```

## HTTP 接口

`/v1/chat/completions`（OpenAI 兼容）、`/v1/memories`、`/v1/retrieve`、`/v1/goal`、`/v1/focus`。
见 `docs/api.md`。

## 基准结果（skill 0.5 → 1.0）

| 指标 | skill=0.5 | skill=1.0 |
|---|---|---|
| 记忆 recall@1 | 0.04 | 1.00 |
| 记忆 recall@5 | 0.54 | 1.00 |
| 目标完成率 | 0.03 | 1.00 |
| 坚持度 persistence | 0.40 | 1.00 |

## 目录

```
museforge/
  memory/     主动记忆：编码/打分/存储/检索/巩固
  focus/      主动专注：目标/规划/追踪/障碍/探索
  engine/     MuseAgent 动作循环
  model/      五后端（mock/cpu/openai/vllm/transformers）
  train/      单调 skill 训练
  bench/      记忆召回 + 专注基准
  serving/    stdlib HTTP（OpenAI 兼容）
  integrations/ LangChain / MCP
docs/         架构/记忆/专注/训练/API 详解
prompts/      可复用提示词模板
recipes/      四类落地配方
deploy/       Docker / docker-compose / K8s / Helm / CI
```

## License

Apache-2.0
