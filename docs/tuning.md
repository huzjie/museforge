# 调优指南

## 记忆召回率低？

- 提高 `w_rel`（更看重相关性）或调大 `top_k`。
- 换真实句向量 `Encoder`（当前是 md5 伪随机向量，只适合做参考/回归）。
- 检查 `half_life_hours`：新近度半衰期过长会压制旧但重要的记忆。

## 专注度一直低？

- 调大 `persistence_budget`（允许更多尝试）。
- 调低 `difficulty_threshold`（更早触发替代路径）。
- 检查子目标分解是否过大——`max_subgoals` 太大时单步更难完成。

## 内存占用高？

- 降 `max_episodes / max_semantic`。
- 调小 `consolidate_after`，更早蒸馏旧的 episodic。
