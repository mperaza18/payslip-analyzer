# CLAUDE.md — Payslip Analyzer

Guía de contexto para Claude Code en este proyecto.

---

## Qué es este proyecto

**Payslip Analyzer** es un MVP que permite subir nóminas CFDI mexicanas (XML + PDF) y obtener:

- Extracción estructurada de percepciones, deducciones y otros pagos
- Agregaciones por periodo (quincena / mes / año)
- Resumen en lenguaje natural generado por LLM

Stack: FastAPI · SQLModel · SQLite · Ollama (o Azure OpenAI) · React + Vite + Tailwind v4 + Recharts.

---

## Estructura del monorepo

```text
payslip-analyzer/
├── backend/app/
│   ├── main.py       # FastAPI app, CORS, startup hook
│   ├── config.py     # Settings via pydantic-settings (.env)
│   ├── db.py         # Engine, init_db(), vista SQL `periods`
│   ├── models/       # SQLModel tables: Payslip, LineItem
│   ├── schemas/      # Pydantic DTOs (request / response)
│   ├── services/     # llm_client.py, xml_parser.py (futuro)
│   └── routers/      # upload.py, payslips.py, summary.py (futuro)
├── frontend/src/     # React app (creada con Vite)
├── uploads/          # gitignored — PDFs y XMLs de usuarios
└── data/             # gitignored — payslips.db SQLite
```

---

## Comandos clave

```bash
# Backend (desde backend/)
source .venv/bin/activate
uvicorn app.main:app --reload --port 8000
pytest tests/ -v

# Frontend (desde frontend/)
npm run dev
npm run build
```

---

## Convenciones de código

### Backend (Python)

- Configuración **siempre** a través de `app/config.py` → `settings`. Nunca `os.environ` directo.
- Modelos de DB en `app/models/`, DTOs de API en `app/schemas/` — no mezclar.
- Rutas registradas en `app/main.py` vía `app.include_router(...)`.
- Sesión de DB inyectada con `Depends(get_session)` — nunca crear `Session` manualmente en routers.
- El proveedor LLM se accede siempre vía `get_llm()` — nunca instanciar `OllamaClient` / `AzureOpenAIClient` directamente.

### Frontend (TypeScript)

- Tailwind v4: usar `@import "tailwindcss"` en CSS, plugin `@tailwindcss/vite` en `vite.config.ts`. Sin `tailwind.config.js`.
- URL base del backend configurada en un único lugar (ej. `src/api/client.ts`).
- Recharts para todas las visualizaciones de datos numéricos.

---

## Variables de entorno

El backend lee desde `backend/.env` (gitignored). El archivo de referencia es `backend/.env.example`.

| Variable           | Cuándo importa                        |
|--------------------|---------------------------------------|
| `LLM_PROVIDER`     | Siempre — define qué cliente se usa   |
| `OLLAMA_*`         | Solo si `LLM_PROVIDER=ollama`         |
| `AZURE_OPENAI_*`   | Solo si `LLM_PROVIDER=azure`          |
| `DATABASE_URL`     | Apunta a `data/payslips.db`           |
| `CORS_ORIGINS`     | Debe incluir el puerto del frontend   |

---

## Decisiones de arquitectura

| Decisión | Razón |
|----------|-------|
| SQLite en lugar de Postgres | MVP local; sin infraestructura adicional |
| `periods` como vista SQL | Siempre derivable de `payslip`; evita doble escritura |
| Interfaz `LLMClient` abstracta | Permite cambiar entre Ollama y Azure sin tocar el pipeline |
| `uuid_timbre` como PK de `Payslip` | Garantizado único por el SAT; evita duplicados al re-subir el mismo XML |
| Tailwind v4 | Sin archivo de config; solo plugin Vite y `@import` |

---

## Estado actual (Fase 1)

- [x] Estructura del monorepo (`chore: bootstrap monorepo layout`)
- [ ] Backend FastAPI con health check y CORS (Paso 2)
- [ ] Frontend React + Vite + Tailwind (Paso 3)
- [ ] Capa LLM abstracta (Paso 4)
- [ ] Esquema SQLite con SQLModel (Paso 5)

---

## Lo que NO está aquí todavía

- Parser XML CFDI (Fase 2)
- Endpoints de upload y consulta (Fase 3)
- Dashboard con gráficas Recharts (Fase 4)
- Resumen LLM por periodo (Fase 5)

No implementar nada de las fases 2-5 hasta que el criterio de éxito de la Fase 1 esté verificado:
`/health` responde, frontend pinta el JSON, LLM responde en tiempo razonable, SQLite tiene las 3 tablas.
