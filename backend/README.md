# EviRank-X Backend

This backend provides a production-oriented Flask API scaffold for the EviRank-X recruitment intelligence platform. It exposes Swagger documentation, health checks, authentication stubs, job analysis, candidate management, ranking workflows, analytics, explainability, and supporting modules for search, uploads, notifications, reports, evidence, SHAP, and comparison.

## Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## API Docs

Open http://localhost:5000/swagger after starting the app.

## Tests

```bash
pytest -q
```
