# 研究智能体配方

- **场景**：长线调研，跨会话累积线索。
- **记忆策略**：每个线索走 `episodic`，定期 `consolidate_after=100` 蒸馏成观点；
  `top_k=8`、`token_budget=2048`、`w_rel=0.6`（调研更看重相关性）。
- **专注目标**：一个研究问题一个 goal，卡点用 `prompts/difficulty_handling.md` 给替代检索方向。
