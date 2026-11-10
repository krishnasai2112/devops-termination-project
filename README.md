# DevOps Termination Project

A locally deployed, containerized Flask application demonstrating modern DevOps practices using Docker, Kubernetes, Helm, GitHub Actions, Prometheus, Grafana, Loki, and Grafana Alloy.

## Project Overview

This project implements a DevOps workflow for a Python Flask web application, from containerization and automated testing to Kubernetes deployment, monitoring, centralized logging, autoscaling, and failure recovery.

The infrastructure runs locally on Minikube, avoiding cloud infrastructure costs.

## Technology Stack

| Category | Technologies |
|---|---|
| Application | Python 3.11, Flask |
| Containerization | Docker |
| Orchestration | Kubernetes, Minikube |
| Package Management | Helm |
| CI Pipeline | GitHub Actions |
| Security | Trivy vulnerability scanning |
| Metrics | Prometheus |
| Visualization | Grafana |
| Centralized Logging | Grafana Loki, Grafana Alloy |
| Networking | Kubernetes Services, NGINX Ingress |
| Scaling | Kubernetes Horizontal Pod Autoscaler |

## Architecture

```text
                      Developer
                          |
                          v
                     GitHub Repo
                          |
                          v
                 GitHub Actions CI
                 - Unit Testing
                 - Docker Build
                 - Smoke Testing
                 - Trivy Scanning
                          |
                          v
                 Local Kubernetes
                     (Minikube)
                          |
                          v
                    NGINX Ingress
                          |
                          v
                   Flask Service
                          |
                 +--------+--------+
                 |                 |
                 v                 v
             Flask Pod 1       Flask Pod 2
                 |                 |
                 +--------+--------+
                          |
                  Horizontal Pod
                    Autoscaler

Observability:
Flask Metrics --> Prometheus --> Grafana
Flask Logs ----> Alloy -------> Loki --> Grafana
```

Note: GitHub Actions runs CI on hosted runners. Deployment to local Minikube is performed separately; the CI workflow does not automatically deploy into the local cluster.

## Application Endpoints

| Endpoint | Purpose |
|---|---|
| `/` | Flask application homepage |
| `/health` | Application liveness endpoint |
| `/ready` | Application readiness endpoint |
| `/metrics` | Prometheus metrics endpoint |

## Key Features

- Dockerized Python Flask application
- Kubernetes Deployment with multiple replicas
- Liveness and readiness probes
- Kubernetes Service and NGINX Ingress
- CPU-based horizontal autoscaling
- Helm installation, upgrades, and rollbacks
- GitHub Actions CI pipeline
- Automated unit tests and container smoke tests
- Trivy container vulnerability scanning
- Prometheus metrics collection
- Grafana monitoring dashboard
- Centralized logging through Alloy and Loki
- Kubernetes rolling updates and automatic pod recovery
- Load testing and automatic scale-up/scale-down

## Prerequisites

Install the following tools before running the project:

- Docker
- Minikube
- kubectl
- Helm
- Python 3.11
- Git

## Run the Application with Docker

Build the image:

```bash
docker build -t devops-flask-app:local .
```

Run the container:

```bash
docker run --rm -p 5000:5000 devops-flask-app:local
```

Test the health endpoint:

```bash
curl http://localhost:5000/health
```

Expected response:

```json
{"status":"ok"}
```

## Deploy to Kubernetes with Minikube

Start the local Kubernetes cluster:

```bash
minikube start --driver=docker
```

Build the application image inside Minikube:

```bash
minikube image build -t devops-flask-app:v3 .
```

Install the Helm application:

```bash
helm upgrade --install flask-demo helm/flask-app \
  --namespace default \
  --wait
```

Verify the application:

```bash
kubectl get pods -l app=flask-demo-app
kubectl get svc flask-demo-service
kubectl get hpa flask-demo-hpa
```

Access the application through port forwarding:

```bash
kubectl port-forward svc/flask-demo-service 8080:5000
```

Open http://localhost:8080 in your browser.

## Kubernetes Ingress

Enable the NGINX Ingress controller:

```bash
minikube addons enable ingress
```

Apply the application's Ingress manifest:

```bash
kubectl apply -f k8s/flask-demo-ingress.yaml
```

For Docker-driver Minikube on macOS, run the tunnel in a separate Terminal:

```bash
minikube tunnel
```

Verify the route:

```bash
curl -H 'Host: flask-demo.local' http://127.0.0.1/health
```

The tunnel must remain running while testing.

## Continuous Integration

The GitHub Actions pipeline is defined in:

```text
.github/workflows/ci-cd.yml
```

The workflow performs:

1. Source checkout
2. Python dependency installation
3. Unit tests
4. Docker image build
5. Application health smoke test
6. Trivy vulnerability scanning

The workflow validates changes but does not automatically deploy to the local Minikube cluster.

## Monitoring and Centralized Logging

Monitoring configuration files are stored in:

```text
monitoring/
├── prometheus-values.yaml
├── grafana-values.yaml
├── loki-values.yaml
├── alloy-values.yaml
└── grafana-dashboard.json
```

Install Prometheus:

```bash
helm upgrade --install prometheus prometheus-community/prometheus \
  --namespace monitoring \
  --create-namespace \
  -f monitoring/prometheus-values.yaml
```

Install Grafana:

```bash
helm upgrade --install grafana grafana-community/grafana \
  --namespace monitoring \
  -f monitoring/grafana-values.yaml
```

Install Loki:

```bash
helm upgrade --install loki grafana-community/loki \
  --namespace monitoring \
  -f monitoring/loki-values.yaml
```

Install Grafana Alloy:

```bash
helm upgrade --install alloy grafana/alloy \
  --namespace monitoring \
  -f monitoring/alloy-values.yaml
```

Helm repositories must be configured before these installations.

Grafana visualizes Prometheus metrics and queries application logs stored in Loki.

## Reliability Tests

The following capabilities were verified locally:

| Test | Observed Result |
|---|---|
| Pod deletion and self-healing | Replacement pod created automatically |
| Rolling update | New pods deployed successfully |
| Helm upgrade | Release revision increased |
| Helm rollback | Previous release configuration restored |
| CPU load generation | CPU utilization reached approximately 93% |
| HPA scale-up | Replicas increased from 2 to 5 |
| HPA scale-down | Replicas returned from 5 to 2 |
| Post-test health check | Flask returned HTTP 200 |

## Project Scope

This is a local educational DevOps demonstration.

Production improvements would include managed persistent storage, authenticated observability services, TLS, secrets management, deployment environments, and a complete CD pipeline.

## Helm Repository Setup

Add the required Helm repositories before installing the monitoring stack:

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana-community https://grafana-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```

Tested chart versions:

| Component | Chart Version |
|---|---|
| Prometheus | 29.47.0 |
| Grafana | 14.4.0 |
| Loki | 21.1.3 |
| Alloy | 1.15.0 |
