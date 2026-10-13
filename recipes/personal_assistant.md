# 个人助理配方

- **场景**：跨会话记住用户偏好，回答问题/写材料。
- **记忆策略**：偏好/事实走 `semantic`（importance 0.8+），一次性事件走 `episodic`；
  `top_k=5`、`token_budget=1024`、`w_rel=0.5 w_rec=0.15 w_imp=0.25 w_freq=0.1`。
- **专注目标**：`max_subgoals=6`，长任务用 `persistence_budget=12`。
- **提示词**：`prompts/memory_retrieval.md` + `prompts/agent_system.md`。
- **示例**：`examples/agent_demo.py`（见 examples 目录）。
