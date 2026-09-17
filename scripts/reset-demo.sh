#!/usr/bin/env bash
# Reset the demo database back to the seeded starting state.
# Usage: scripts/reset-demo.sh
set -euo pipefail

cd "$(dirname "$0")/.."

rm -f backend/compliance.db
echo "Removed backend/compliance.db (SQLite). It is re-created and seeded on next backend start."
echo "Start the backend with: cd backend && . .venv/bin/activate && uvicorn app.main:app --port 8000"
