# 配置变体

- `default.yaml`：默认，内置于包内 `museforge/configs/default.yaml`
- `small.yaml`：小内存/低预算（端侧）
- `large.yaml`：大内存/高预算 + openai 后端模板

用 `python -m museforge.cli --config configs/large.yaml doctor` 指定。
