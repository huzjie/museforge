# FAQ

**Q：为什么零依赖？**
A：参考实现要能在任何环境直接 `python -m museforge.cli doctor` 跑通，不依赖 numpy/pyyaml/requests。
   嵌入用 md5 伪随机向量，配置用内置 yamlish 回退。

**Q：怎么接真实 LLM？**
A：设 `model.name=openai` 并填 `api_base/api_key/model_id`，或直接把 `MuseAgent` 的 `backend`
   换成你自己的实现（实现 `generate/rank_memories/try_subgoal/persist_after_failure` 四个方法）。

**Q：记忆会一直涨吗？**
A：不会。`max_episodes/max_semantic` 做硬上限，`consolidate_after` 触发旧的 episodic 蒸馏成
   semantic 事实。

**Q：专注度有什么用？**
A：它是一个可测的标量，用来判断「这个智能体能不能扛住长任务」。可做回归护栏，也能做路由
   信号（低专注度任务转人工或换更大模型）。
