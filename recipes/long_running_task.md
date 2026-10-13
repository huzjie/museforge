# 长任务执行配方

- **场景**：跨多轮、跨会话推进一个硬目标（如项目迁移）。
- **专注目标**：`persistence_budget` 调大（20+），`staleness_threshold=3` 触发替代路径。
- **关键**：每轮结束调用 `focus_score`，低于阈值（如 0.4）时介入——转人工或换策略。
- **提示词**：`prompts/focus_planning.md` + `prompts/difficulty_handling.md`。
