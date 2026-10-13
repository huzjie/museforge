# 客服智能体配方

- **场景**：记住用户历史工单、产品偏好，缩短复述。
- **记忆策略**：工单编号/结论走 `semantic`，`importance` 按解决满意度映射（0.3-1.0）；
  `half_life_hours=72`（客服场景新近度更短半衰期）。
- **专注目标**：单个工单为一个 goal，子目标 = 定位/复现/解决/回访。
- **提示词**：`prompts/memory_retrieval.md` + `prompts/difficulty_handling.md`（卡点转人工）。
