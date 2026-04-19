# Phase 1 Completion — Design Spec

**Date:** 2026-04-19
**Scope:** Two remaining Phase 1 items: SQLite schema (backend) + React app shell (frontend)
**Approach:** Schema first, then frontend (Option A — independently verifiable steps)

---

## Context

Phase 1 Foundation is partially complete:

| Step | Status |
|---|---|
| Monorepo structure | ✅ Done |
| FastAPI backend (config, db, LLM client, `/health`) | ✅ Done |
| LLM abstraction layer (Ollama / Azure) | ✅ Done |
| **SQLite schema (`payslips`, `line_items`, `periods`)** | ❌ To implement |
| **Frontend React + Vite + Tailwind v4 shell** | ❌ To implement |

Phase 2–5 are blocked until Phase 1's success criterion is met:
> `/health` responds · frontend renders the JSON · LLM responds · SQLite has the 3 tables

---

## Step 1 — SQLite Schema

### Files

- `backend/app/models/payslip.py` — `Payslip` SQLModel table
- `backend/app/models/line_item.py` — `LineItem` SQLModel table
- `backend/app/models/__init__.py` — exports both classes (triggers SQLModel metadata registration)
- `backend/app/db.py` — add `periods` view creation after `SQLModel.metadata.create_all()`

### `Payslip` table

| Field | Type | Notes |
|---|---|---|
| `uuid_timbre` | `str` | PK — UUID from SAT timbre fiscal; prevents duplicate uploads |
| `employee_name` | `str` | |
| `period_start` | `date` | |
| `period_end` | `date` | |
| `total_perceptions` | `float` | |
| `total_deductions` | `float` | |
| `net_pay` | `float` | |
| `created_at` | `datetime` | Default = `datetime.utcnow` |

### `LineItem` table

| Field | Type | Notes |
|---|---|---|
| `id` | `int` | PK, auto-increment |
| `payslip_id` | `str` | FK → `payslip.uuid_timbre` |
| `type` | `str` | `"perception"` or `"deduction"` |
| `code` | `str` | CFDI concept code |
| `description` | `str` | |
| `amount` | `float` | |

### `periods` SQL view

Created in `db.py` after `SQLModel.metadata.create_all()` using a raw `text()` statement:

```sql
CREATE VIEW IF NOT EXISTS periods AS
SELECT strftime('%Y', period_start) AS year,
       strftime('%m', period_start) AS month,
       COUNT(*)                     AS payslip_count,
       SUM(total_perceptions)       AS total_perceptions,
       SUM(total_deductions)        AS total_deductions,
       SUM(net_pay)                 AS net_pay
FROM payslip
GROUP BY year, month
```

### Success check

```bash
cd backend && source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
# verify in data/payslips.db:
sqlite3 ../data/payslips.db ".tables"
# expected: line_item  payslip  periods
```

---

## Step 2 — Frontend Shell

### Scaffolding

```bash
cd frontend
npm create vite@latest . -- --template react-ts
npm install tailwindcss @tailwindcss/vite
npm install recharts
```

Tailwind v4 config: add `@tailwindcss/vite` plugin to `vite.config.ts`; use `@import "tailwindcss"` in `index.css`. No `tailwind.config.js`.

### File structure

```
frontend/src/
├── api/
│   └── client.ts          # BASE_URL const + fetchHealth()
├── components/
│   ├── Navbar.tsx          # "Payslip Analyzer" header + HealthBadge
│   └── HealthBadge.tsx     # calls /health, shows status dot + JSON
├── pages/
│   └── Dashboard.tsx       # placeholder cards: Upload / Summary / Charts
├── App.tsx                 # composes Navbar + Dashboard
├── main.tsx                # Vite entry point
└── index.css               # @import "tailwindcss"
```

### `client.ts`

Single source of truth for the backend URL:

```ts
const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
export const fetchHealth = () => fetch(`${BASE_URL}/health`).then(r => r.json())
```

### UI layout

- **Navbar** — "Payslip Analyzer" title (left) + `HealthBadge` (right)
- **HealthBadge** — auto-calls `/health` on mount; shows green dot + raw JSON when backend is up, red dot + error message when down
- **Dashboard** — three placeholder cards:
  - "Upload" — grayed out, "Coming in Phase 3"
  - "Summary" — grayed out, "Coming in Phase 4"
  - "Charts" — grayed out, "Coming in Phase 4"

### Success check

```bash
cd frontend && npm run dev
# open http://localhost:5173
# Navbar shows green dot + {"status":"ok","llm_provider":"ollama"}
```

---

## Phase 1 Success Criterion (full)

All four must pass before starting Phase 2:

- [ ] `curl http://localhost:8000/health` → `{"status":"ok","llm_provider":"..."}`
- [ ] Frontend loads at `http://localhost:5173` and shows the health JSON
- [ ] `curl http://localhost:8000/llm/ping` returns a response from the LLM
- [ ] `sqlite3 ../data/payslips.db ".tables"` shows `line_item payslip periods`
