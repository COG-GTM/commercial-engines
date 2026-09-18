# Commercial Engines — Coding Standards

Applies to `nandu-cog-demos/commercial-engines` (Fleet Compliance Portal). Devin reads this file at the start of every feature session and must comply; deviations are called out in the PR.

## 1. General
- Small, focused changes. One feature per branch/PR; no drive-by refactors or reformatting.
- No new dependencies without a stated reason in the PR.
- Prefer clarity over cleverness. Rely on good names; comments only for non-obvious *why*, never for *what* or for describing the change.
- Never modify or delete existing tests to make them pass.
- Every behaviour described in the spec maps to a test or a visible UI behaviour.

## 2. Python / FastAPI (backend)
- Python 3.11+ syntax; full type hints on all function signatures (`def f(x: int) -> str`). Use `X | None`, not `Optional[X]`.
- `ruff check app tests` must pass with zero warnings; do not add `# noqa` without a comment explaining why.
- Naming: `snake_case` for functions, variables, modules, DB columns; `PascalCase` for classes and Pydantic models; `UPPER_SNAKE` for constants.
- Routes live in `app/main.py`, versioned under `/api/v1`. Handlers stay thin (≤ ~30 lines): parse → call helper → return schema. Business rules go in a helper function in the same module, or in `app/<feature>.py` when they exceed ~40 lines.
- Pydantic response models in `app/schemas.py`; JSON fields are `camelCase` via the existing alias config. Never return raw ORM objects or dicts.
- SQLAlchemy 2 style (`select()` + `session.execute`/`scalars`); no legacy `session.query`. No raw SQL.
- Use `HTTPException` with an explicit status code and a structured `detail` (dict/list, not a bare string) for domain errors. 404 for missing resources, 409 for business-rule conflicts, 422 for validation.
- Dates: store as `date`/`datetime`, compute "today" once per request via a single helper so tests can control it. No `datetime.now()` scattered through handlers.
- Seed data (`app/seed.py`) is the demo contract. Change it only when the spec requires; update `docs/tickets/` in the same PR.

## 3. Tests (backend)
- `pytest -q` must pass. Tests live in `backend/tests/`, one file per feature area (`test_<feature>.py`) using the shared `client` fixture.
- Test names read as sentences: `test_release_gate_blocks_when_mandatory_sb_overdue`.
- Every endpoint change has: a happy-path test, an empty/none test, and one test per negative rule stated in the spec.
- Assert on the full relevant response shape (status code + key fields), not just status codes. Use seeded serials/SB numbers rather than inventing fixtures.
- No sleeps, no network, no test order dependence.

## 4. TypeScript / React (frontend)
- Strict TypeScript; `npm run build` (tsc + vite) must pass. No `any`, no `as unknown as`, no `// @ts-ignore`.
- Every API response has an explicit `interface` in `src/api.ts` mirroring the backend schema (camelCase). All fetches go through `src/api.ts` + `useApi.ts`; no `fetch()` inside components.
- Components: function components only, `PascalCase` file and component names, one page component per file under `src/pages/`. Hooks at top level, prefixed `use`.
- Derive nothing in the UI that the API already provides (e.g. overdue flags come from the backend). No business rules in TypeScript.
- Reuse existing classes from `src/styles.css`; add new classes there rather than inline styles. Match the look of neighbouring pages (tables, badges, buttons).
- Handle the three states explicitly in every data view: loading, error, empty.
- Accessible by default: buttons are `<button>`, tables have headers, dialogs trap focus and close on Escape.

## 5. Git & PRs
- Branch: `devin/<unix-timestamp>-<short-slug>`. Never push to `main`.
- Commits: imperative mood, ≤ 72-char subject, logical units (backend / tests / frontend). Add files explicitly; never `git add .`.
- PR title: `feature: <TICKET-ID> <short description>`.
- PR body: summary (what + why), assumptions, test evidence (commands run + screenshot), follow-ups, and the final line `Devin-Org: engineering`.
- CI (`ruff`, `pytest`, `tsc`+`vite build`) must be green before requesting review.

## 6. Verification before hand-off
- Run `make dev`, exercise the new endpoint with `curl` against seeded data, and record a browser walkthrough of all main pages plus the new feature.
- Post PR link + recording to the originating Slack thread.
