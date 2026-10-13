# Deployment

## Docker

    docker build -f deploy/Dockerfile -t museforge .
    docker run -p 8000:8000 museforge

## docker-compose

    docker compose -f deploy/docker-compose.yml up --build

## Kubernetes

    kubectl apply -f deploy/k8s/deployment.yaml
    kubectl apply -f deploy/k8s/service.yaml

## Helm

    helm install museforge deploy/helm

The server exposes the OpenAI-compatible endpoint at `/v1/chat/completions`.
