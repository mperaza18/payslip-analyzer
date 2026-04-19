# Payslip Analyzer

Monorepo con backend FastAPI + frontend React/Vite para análisis de nóminas CFDI.

## Desarrollo rápido

```bash
# Backend
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend && npm run dev
```

## Estructura

```
payslip-analyzer/
├── backend/   # FastAPI + SQLModel + LLM client
├── frontend/  # React + Vite + Tailwind + Recharts
├── uploads/   # PDFs y XMLs (gitignored)
└── data/      # SQLite DB (gitignored)
```
