.PHONY: dev backend frontend test lint install clean

install:
	cd backend && python3 -m venv .venv && . .venv/bin/activate && pip install -e '.[dev]'
	cd frontend && npm install

backend:
	cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000

frontend:
	cd frontend && npm run dev

# Runs backend and frontend together; Ctrl-C stops both.
dev:
	@echo "backend :8000  |  frontend :5173"
	@trap 'kill 0' INT TERM; \
	( cd backend && . .venv/bin/activate && uvicorn app.main:app --reload --port 8000 ) & \
	( cd frontend && npm run dev ) & \
	wait

test:
	cd backend && . .venv/bin/activate && pytest -q
	cd frontend && npm run build

lint:
	cd backend && . .venv/bin/activate && ruff check app tests

clean:
	rm -f backend/compliance.db
	rm -rf frontend/dist
