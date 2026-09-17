# AGENTS.md

## Layout

- `backend/` — FastAPI app. `app/models.py` (SQLAlchemy), `app/schemas.py`
  (Pydantic, camelCase API shapes), `app/main.py` (routes), `app/seed.py`
  (demo data), `tests/`.
- `frontend/` — React + TS + Vite. Pages under `src/pages/`, typed API client in
  `src/api.ts`.
- `docs/tickets/` — feature specs.

## Build & test

Backend:

```bash
cd backend
python -m venv .venv && . .venv/bin/activate
pip install -e '.[dev]'
pytest -q
ruff check app tests
```

Frontend:

```bash
cd frontend
npm install
npm run build      # tsc + vite build (also the typecheck gate)
```

Run both with `make dev` from the repo root.

## Conventions

- API paths are versioned under `/api/v1`. JSON fields are **camelCase**
  (see `schemas.py`); DB columns are snake_case.
- Keep route handlers thin; put query logic in the handler or a small helper,
  not in the models.
- Add or update tests for any endpoint change and keep `pytest -q` and
  `npm run build` green before pushing.
- Seed data is the contract for the demo. If you change engine serials, SB
  numbers, ranges or CSNs, update `docs/tickets/` accordingly.
- The `postgres` profile requires Docker (`docker compose up -d db`); default
  runs on SQLite with no external services.
