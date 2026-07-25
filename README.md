# ML Docker Demo

A minimal, production-patterned ML serving pipeline: train a model, package it in
Docker, and serve predictions over a REST API. Built as a reference implementation
for containerized MLOps workflows, following current best practices for
reproducibility and security rather than shortcuts.

## What this is

A linear regression model (scikit-learn) trained on synthetic data, served via
FastAPI, containerized with Docker, and orchestrated locally with Docker Compose.
The goal is a correct, minimal soup-to-nuts pipeline that mirrors how a real
service would be deployed to AWS ECS/Fargate or similar — without the AWS bill.

## Stack

- **Model**: scikit-learn `LinearRegression`
- **Serving**: FastAPI + Pydantic (request/response validation)
- **Packaging**: Docker (non-root user, pinned deps via `uv.lock`)
- **Orchestration**: Docker Compose (healthchecks, restart policy)
- **Environment**: managed with [`uv`](https://github.com/astral-sh/uv)

## Design decisions

- **Model artifact stored as JSON, not pickle.** Pickle can execute arbitrary
  code on load; for a linear model, plain coefficients in JSON are safer,
  human-readable, and language-agnostic.
- **Non-root container user.** Reduces blast radius if the container is
  ever compromised.
- **Locked dependencies (`uv.lock`).** Builds are reproducible — no
  silent version drift between machines.
- **Healthcheck baked into the image.** Matches how ECS/Fargate or
  Kubernetes would monitor container liveness in production.

## Project structure

ml-docker-demo/
├── train.py # trains the model, writes model.json
├── app.py # FastAPI service
├── model.json # trained model coefficients
├── pyproject.toml
├── uv.lock
├── Dockerfile
├── docker-compose.yml
└── .dockerignore

## Running it

```bash
docker compose up --build
```

API available at `http://localhost:8000`.

### Endpoints

| Method | Path        | Description                    |
|--------|-------------|--------------------------------|
| GET    | `/health`   | Liveness check                 |
| POST   | `/predict`  | Returns a prediction for 4 input features |

**Example request:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"x1": 1, "x2": 2, "x3": 3, "x4": 4}'
```

**Example response:**

```json
{"prediction": 18.61}
```

## Retraining the model

```bash
uv run python train.py
```

Regenerates `model.json` from a fresh synthetic dataset (fixed seed for
reproducibility).

## Roadmap

- [ ] Push image to a container registry (ECR / Docker Hub)
- [ ] Deploy to a single EC2 instance or minimal Fargate task
- [ ] Add CI (GitHub Actions: lint, test, build image on push)
- [ ] Add basic auth / rate limiting before any public exposure
- [ ] Swap in a model registry (MLflow) if versioning multiple models

## License

MIT