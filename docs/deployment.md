# 部署

见 `deploy/README.md`。核心：`deploy/Dockerfile`、`deploy/docker-compose.yml`、
`deploy/k8s/`、`deploy/helm/`、`.github/workflows/ci.yml`。

服务暴露 OpenAI 兼容端点 `/v1/chat/completions`，可直接接到任意支持 OpenAI 协议的客户端。
