# Contributing

1. 保持零依赖：新增能力优先用标准库实现，或做成可选的集成适配器。
2. 所有新增模块配 `tests/` 单测（`python -m unittest discover -s tests -t .`）。
3. 改动打分/训练信号后，跑 `python -m museforge.cli bench` 确认曲线仍单调。
4. 文档写「怎么做/思路/提示词」，不写资讯式总结。
