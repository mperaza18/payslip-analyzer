# Phase 1 Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Complete the two remaining Phase 1 items — SQLite schema and React app shell — so every Phase 1 success criterion is met.

**Architecture:** Backend: two SQLModel table classes (`Payslip`, `LineItem`) imported in `db.py` to register their metadata before `create_all()`, plus a raw-SQL `periods` view created in `init_db()`. Frontend: Vite `react-ts` scaffold wired with Tailwind v4 (zero config file) and a one-page shell that auto-calls `/health` on mount.

**Tech Stack:** Python 3.12 · SQLModel · SQLite · pytest | React 18 · TypeScript · Vite 5 · Tailwind v4 · Recharts

---

## File Map

### Backend

| File | Action | Responsibility |
|---|---|---|
| `backend/tests/__init__.py` | Create | Makes `tests/` a package |
| `backend/tests/test_db_schema.py` | Create | Verifies 3 DB objects after `init_db()` |
| `backend/app/models/payslip.py` | Create | `Payslip` SQLModel table |
| `backend/app/models/line_item.py` | Create | `LineItem` SQLModel table |
| `backend/app/models/__init__.py` | Modify | Re-export both classes |
| `backend/app/db.py` | Modify | Import models + create `periods` view in `init_db()` |

### Frontend

| File | Action | Responsibility |
|---|---|---|
| `frontend/` | Scaffold | Vite `react-ts` template (replaces `.gitkeep`) |
| `frontend/vite.config.ts` | Modify | Add `@tailwindcss/vite` plugin |
| `frontend/src/index.css` | Replace | `@import "tailwindcss"` only |
| `frontend/src/api/client.ts` | Create | `BASE_URL` constant + `fetchHealth()` |
| `frontend/src/components/HealthBadge.tsx` | Create | Calls `/health`, shows status dot + JSON |
| `frontend/src/components/Navbar.tsx` | Create | App title + `HealthBadge` in header |
| `frontend/src/pages/Dashboard.tsx` | Create | Three placeholder cards |
| `frontend/src/App.tsx` | Replace | Composes `Navbar` + `Dashboard` |

---

## Task 1: SQLite schema (backend)

**Files:**
- Create: `backend/tests/__init__.py`
- Create: `backend/tests/test_db_schema.py`
- Create: `backend/app/models/payslip.py`
- Create: `backend/app/models/line_item.py`
- Modify: `backend/app/models/__init__.py`
- Modify: `backend/app/db.py`

- [ ] **Step 1: Verify pytest is available**

```bash
cd backend && source .venv/bin/activate && pytest --version
```

Expected: `pytest 7.x.x` or higher. If not found: `pip install pytest`

- [ ] **Step 2: Create tests package and write the failing tests**

```bash
mkdir -p backend/tests && touch backend/tests/__init__.py
```

Create `backend/tests/test_db_schema.py`:

```python
import pytest
from sqlmodel import create_engine, text
import app.db as db_module


@pytest.fixture()
def patched_db(tmp_path, monkeypatch):
    test_engine = create_engine(f"sqlite:///{tmp_path}/test.db")
    monkeypatch.setattr(db_module, "engine", test_engine)
    yield test_engine


def test_payslip_table_created(patched_db):
    db_module.init_db()
    with patched_db.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='payslip'")
        ).first()
    assert row is not None, "payslip table should exist after init_db()"


def test_line_item_table_created(patched_db):
    db_module.init_db()
    with patched_db.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='line_item'")
        ).first()
    assert row is not None, "line_item table should exist after init_db()"


def test_periods_view_created(patched_db):
    db_module.init_db()
    with patched_db.connect() as conn:
        row = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='view' AND name='periods'")
        ).first()
    assert row is not None, "periods view should exist after init_db()"
```

- [ ] **Step 3: Run tests — expect FAIL**

```bash
cd backend && source .venv/bin/activate && pytest tests/test_db_schema.py -v
```

Expected: 3 FAILED — `AssertionError: payslip table should exist after init_db()` (models not registered yet)

- [ ] **Step 4: Create `backend/app/models/payslip.py`**

```python
from datetime import date, datetime
from sqlmodel import Field, SQLModel


class Payslip(SQLModel, table=True):
    uuid_timbre: str = Field(primary_key=True)
    employee_name: str
    period_start: date
    period_end: date
    total_perceptions: float
    total_deductions: float
    net_pay: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

- [ ] **Step 5: Create `backend/app/models/line_item.py`**

```python
from typing import Optional
from sqlmodel import Field, SQLModel


class LineItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    payslip_id: str = Field(foreign_key="payslip.uuid_timbre")
    type: str
    code: str
    description: str
    amount: float
```

- [ ] **Step 6: Update `backend/app/models/__init__.py`**

```python
from .payslip import Payslip
from .line_item import LineItem

__all__ = ["Payslip", "LineItem"]
```

- [ ] **Step 7: Replace `backend/app/db.py`**

```python
from sqlmodel import SQLModel, create_engine, Session, text
from .config import settings
from .models import Payslip, LineItem  # noqa: F401 — registers SQLModel metadata

engine = create_engine(settings.DATABASE_URL, echo=False)

_PERIODS_VIEW_SQL = """\
CREATE VIEW IF NOT EXISTS periods AS
SELECT strftime('%Y', period_start) AS year,
       strftime('%m', period_start) AS month,
       COUNT(*)                     AS payslip_count,
       SUM(total_perceptions)       AS total_perceptions,
       SUM(total_deductions)        AS total_deductions,
       SUM(net_pay)                 AS net_pay
FROM payslip
GROUP BY year, month
"""


def init_db() -> None:
    SQLModel.metadata.create_all(engine)
    with engine.connect() as conn:
        conn.execute(text(_PERIODS_VIEW_SQL))
        conn.commit()


def get_session():
    with Session(engine) as session:
        yield session
```

- [ ] **Step 8: Run tests — expect PASS**

```bash
cd backend && source .venv/bin/activate && pytest tests/test_db_schema.py -v
```

Expected:
```
tests/test_db_schema.py::test_payslip_table_created PASSED
tests/test_db_schema.py::test_line_item_table_created PASSED
tests/test_db_schema.py::test_periods_view_created PASSED

3 passed in 0.xxs
```

- [ ] **Step 9: Commit**

```bash
git add backend/tests/ backend/app/models/ backend/app/db.py
git commit -m "feat(db): add Payslip + LineItem models and periods view"
```

---

## Task 2: Scaffold Vite + React + TypeScript

**Files:**
- Replace: `frontend/` (scaffold over `.gitkeep`)

- [ ] **Step 1: Remove the placeholder and scaffold**

```bash
cd frontend && rm -f src/.gitkeep
npm create vite@latest . -- --template react-ts
```

When prompted "Target directory is not empty. Remove existing files and continue?" → **Y**

- [ ] **Step 2: Install dependencies (including Recharts for Phase 4)**

```bash
cd frontend && npm install && npm install recharts
```

- [ ] **Step 3: Start the dev server and verify it loads**

```bash
cd frontend && npm run dev
```

Expected: `VITE v5.x.x  ready` and `Local: http://localhost:5173/`. The default Vite+React page should load in the browser. Stop with `Ctrl+C`.

- [ ] **Step 4: Commit**

```bash
git add frontend/
git commit -m "feat(frontend): scaffold Vite react-ts app"
```

---

## Task 3: Configure Tailwind v4

**Files:**
- Modify: `frontend/vite.config.ts`
- Replace: `frontend/src/index.css`
- Delete: `frontend/src/App.css`

- [ ] **Step 1: Install Tailwind v4 packages**

```bash
cd frontend && npm install tailwindcss @tailwindcss/vite
```

- [ ] **Step 2: Replace `frontend/vite.config.ts`**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

- [ ] **Step 3: Replace `frontend/src/index.css` with just the import**

```css
@import "tailwindcss";
```

- [ ] **Step 4: Delete `src/App.css` and add a temporary Tailwind smoke-test to `src/App.tsx`**

```bash
rm frontend/src/App.css
```

Replace the full content of `frontend/src/App.tsx` with:

```tsx
export default function App() {
  return <div className="bg-red-500 p-8 text-2xl text-white">Tailwind works</div>
}
```

- [ ] **Step 5: Start the dev server and verify Tailwind renders**

```bash
cd frontend && npm run dev
```

Open `http://localhost:5173`. Expected: red background, white text reading "Tailwind works". Stop with `Ctrl+C`.

- [ ] **Step 6: Commit**

```bash
git add frontend/vite.config.ts frontend/src/index.css frontend/src/App.tsx
git rm frontend/src/App.css
git commit -m "feat(frontend): configure Tailwind v4"
```

---

## Task 4: Build app shell

**Files:**
- Create: `frontend/src/api/client.ts`
- Create: `frontend/src/components/HealthBadge.tsx`
- Create: `frontend/src/components/Navbar.tsx`
- Create: `frontend/src/pages/Dashboard.tsx`
- Replace: `frontend/src/App.tsx`

- [ ] **Step 1: Create `frontend/src/api/client.ts`**

```typescript
const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export interface HealthResponse {
  status: string
  llm_provider: string
}

export const fetchHealth = (): Promise<HealthResponse> =>
  fetch(`${BASE_URL}/health`).then((r) => {
    if (!r.ok) throw new Error(`HTTP ${r.status}`)
    return r.json()
  })
```

- [ ] **Step 2: Create `frontend/src/components/HealthBadge.tsx`**

```tsx
import { useEffect, useState } from 'react'
import { fetchHealth, type HealthResponse } from '../api/client'

export default function HealthBadge() {
  const [data, setData] = useState<HealthResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchHealth()
      .then(setData)
      .catch((e: Error) => setError(e.message))
  }, [])

  if (error) {
    return (
      <span className="flex items-center gap-1.5 text-sm text-red-400">
        <span className="h-2 w-2 rounded-full bg-red-500" />
        Backend down: {error}
      </span>
    )
  }

  if (!data) {
    return (
      <span className="flex items-center gap-1.5 text-sm text-gray-400">
        <span className="h-2 w-2 animate-pulse rounded-full bg-gray-400" />
        Connecting…
      </span>
    )
  }

  return (
    <span className="flex items-center gap-1.5 text-sm text-green-400">
      <span className="h-2 w-2 rounded-full bg-green-500" />
      <code className="text-xs">{JSON.stringify(data)}</code>
    </span>
  )
}
```

- [ ] **Step 3: Create `frontend/src/components/Navbar.tsx`**

```tsx
import HealthBadge from './HealthBadge'

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between border-b border-gray-700 bg-gray-900 px-6 py-3">
      <span className="text-lg font-semibold text-white">Payslip Analyzer</span>
      <HealthBadge />
    </nav>
  )
}
```

- [ ] **Step 4: Create `frontend/src/pages/Dashboard.tsx`**

```tsx
const cards = [
  { title: 'Upload', description: 'Drag & drop payslip files', phase: 3 },
  { title: 'Summary', description: 'Annual & monthly KPIs', phase: 4 },
  { title: 'Charts', description: 'Stacked bar + pie breakdown', phase: 4 },
]

export default function Dashboard() {
  return (
    <main className="p-6">
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        {cards.map((card) => (
          <div
            key={card.title}
            className="rounded-lg border border-gray-700 bg-gray-800 p-6 opacity-50"
          >
            <h2 className="text-base font-medium text-white">{card.title}</h2>
            <p className="mt-1 text-sm text-gray-400">{card.description}</p>
            <p className="mt-3 text-xs text-gray-500">Coming in Phase {card.phase}</p>
          </div>
        ))}
      </div>
    </main>
  )
}
```

- [ ] **Step 5: Replace `frontend/src/App.tsx`**

```tsx
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Navbar />
      <Dashboard />
    </div>
  )
}
```

- [ ] **Step 6: Start both servers and verify**

Terminal 1 (backend):
```bash
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000
```

Terminal 2 (frontend):
```bash
cd frontend && npm run dev
```

Open `http://localhost:5173`. Expected:
- Dark background (`bg-gray-950`)
- Navbar: "Payslip Analyzer" on the left, green dot + `{"status":"ok","llm_provider":"ollama"}` on the right
- Three grayed-out placeholder cards below (Upload · Summary · Charts)

If the backend is stopped, the badge should show a red dot + "Backend down: Failed to fetch".

- [ ] **Step 7: Verify SQLite tables (final Phase 1 check)**

With the backend running (from Terminal 1 above):
```bash
sqlite3 data/payslips.db ".tables"
```

Expected: `line_item  payslip  periods`

- [ ] **Step 8: Commit**

```bash
git add frontend/src/
git commit -m "feat(frontend): add app shell with Navbar, HealthBadge, and Dashboard"
```

---

## Phase 1 Success Criteria — All Must Pass

- [ ] `curl http://localhost:8000/health` → `{"status":"ok","llm_provider":"..."}`
- [ ] Frontend at `http://localhost:5173` shows health JSON in the navbar
- [ ] `curl http://localhost:8000/llm/ping` returns an LLM response
- [ ] `sqlite3 data/payslips.db ".tables"` → `line_item  payslip  periods`
