# Developer Guide

## Local development

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Testing

```bash
pytest -q
```

## Swagger

Open http://localhost:5000/swagger after launching the backend.

## Extending the backend

1. Add a new namespace module under app/api.
2. Register it in app/api/__init__.py.
3. Add tests in backend/tests.
4. Keep service logic in app/services for reuse.
