# Payslip Analyzer

Monorepo para analizar nóminas CFDI (XML/PDF) con un backend FastAPI y un frontend React.  
Extrae percepciones, deducciones y periodos usando un LLM local (Ollama) o Azure OpenAI.

---

## Prerequisitos globales

| Herramienta | Versión  | Verificar             |
|-------------|----------|-----------------------|
| Python      | 3.11+    | `python --version`    |
| Node.js     | 20 LTS+  | `node --version`      |
| Git         | cualquier| `git --version`       |

> Si tienes menos de 16 GB de RAM, configura `LLM_PROVIDER=azure` en `backend/.env`.

---

## Levantar el proyecto completo

### 1. Clonar y entrar al repo

```bash
git clone <url-del-repo> payslip-analyzer
cd payslip-analyzer
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # edita LLM_PROVIDER y claves si usas Azure
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend (en otra terminal)

```bash
cd frontend
npm install
npm run dev

```

Abre **`http://localhost:5173`** — debe mostrar el JSON del `/health` del backend.

---

## Verificar el stack completo

```bash
# API viva
curl http://localhost:8000/health
# {"status":"ok","llm_provider":"ollama"}

# LLM respondiendo
curl http://localhost:8000/llm/ping
# {"llm_response":{"ok":true}}

# Swagger UI
open http://localhost:8000/docs
```

### Todos los comandos:
```bash
Terminal 1 — Backend:
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000

Terminal 2 — Frontend:
cd frontend
npm run dev

Verificar:
# API
curl http://localhost:8000/health
# → {"status":"ok","llm_provider":"ollama"}

# Tablas SQLite (se crean en el primer arranque)
sqlite3 data/payslips.db ".tables"
# → line_item  payslip  periods

# UI
open http://localhost:5173
# → Navbar con punto verde + JSON del /health

Tests:
cd backend && source .venv/bin/activate && pytest tests/ -v
# → 3 passed
  ```

---

## Estructura del monorepo

```text
payslip-analyzer/
├── backend/          # FastAPI + SQLModel + LLM client
│   ├── app/
│   │   ├── main.py       # entrypoint
│   │   ├── config.py     # settings (pydantic-settings)
│   │   ├── db.py         # engine + init_db
│   │   ├── models/       # tablas SQLModel
│   │   ├── schemas/      # DTOs Pydantic
│   │   ├── services/     # parser XML, llm_client, aggregator
│   │   └── routers/      # upload, payslips, summary
│   └── tests/
├── frontend/         # React 18 + Vite + Tailwind v4 + Recharts
│   └── src/
├── uploads/          # PDFs y XMLs originales (gitignored)
├── data/             # payslips.db SQLite (gitignored)
├── .gitignore
└── README.md         ← estás aquí
```

---

## Documentación por servicio

- [Backend →](backend/README.md) — setup Python, variables de entorno, endpoints, tests
- [Frontend →](frontend/README.md) — setup Node, comandos Vite, estructura de componentes

---

## Fases de desarrollo

| Fase | Descripción                        | Estado      |
|------|------------------------------------|-------------|
| 1    | Foundation setup (monorepo + stack)| ✅ Completa  |
| 2    | Parser XML CFDI                    | Pendiente   |
| 3    | Endpoints REST                     | Pendiente   |
| 4    | UI — dashboard de nóminas          | Pendiente   |
| 5    | Análisis LLM + resumen             | Pendiente   |
