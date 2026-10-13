# 从「全量历史注入」迁移

1. 引入 `MemoryStore` 存 episodic + semantic。
2. 每个回合用 `Retriever.retrieve(query, k, budget)` 取 top-k 而非全量。
3. 设 `consolidate_after` 触发蒸馏，控制长期增长。
4. 用 `focus_score` 做长任务护栏。

迁移收益：长会话上下文不再线性膨胀；跨会话可复用用户偏好；长任务有量化护栏。
