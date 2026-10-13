# 端侧部署配方

- **场景**：手机/树莓派等低资源设备跑个人助理。
- **配置**：用 `configs/small.yaml`（`embed_dim=32`、`token_budget=512`、`top_k=3`）。
- **后端**：`cpu`（skill 固定 1.0，零网络）。
- **持久化**：`persistence_path` 指向本地 json。
