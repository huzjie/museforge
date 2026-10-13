# 架构

museforge 是一个**零依赖**的个人智能体「主动记忆 + 主动专注」引擎，参考 Meta Muse Wonder 的
两大核心能力（Active Memory / Active Focus）做的一个可运行参考实现。

## 模块分层

    museforge/
      config.py           配置（YAML/JSON，内置 yamlish 回退）
      utils/              确定性哈希、向量、文本工具（md5 种子）
      memory/             Active Memory：编码/打分/存储/检索/巩固
      focus/              Active Focus：目标/规划/追踪/障碍/探索
      engine/agent.py     MuseAgent 动作循环（记忆 → 专注 → 生成）
      model/backends.py   五后端（mock/cpu/openai/vllm/transformers）
      train/              单调 skill 训练
      bench/              记忆召回 + 专注坚持度基准
      serving/            stdlib HTTP 服务（OpenAI 兼容）
      integrations/       LangChain / MCP 适配

## 数据流（单轮）

    用户 query
      └─> Retriever.retrieve(query)     # 主动检索 top-k 记忆（token 预算内）
      └─> FocusManager.state(goal)       # 评估进度/卡点/替代路径
      └─> 组装 memory-augmented prompt
      └─> backend.generate(prompt)
      └─> 返回 response + retrieved + consolidated

## 关键设计决策

1. **嵌入用 md5 种子伪随机向量**：零依赖、可复现、够用。生产替换 `Encoder.encode` 即可。
2. **打分 = 相关性 + 新近度 + 重要度 + 频次**（加权和），而非单一相似度。
3. **主动检索替代全量注入**：top-k + token 预算，避免长会话上下文爆炸。
4. **专注度 = 0.5·进度 + 0.3·坚持 + 0.2·自适应**，一个可测的标量。
