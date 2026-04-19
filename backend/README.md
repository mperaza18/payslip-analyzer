# Backend — Payslip Analyzer

FastAPI · SQLModel · SQLite · LLM client (Ollama / Azure OpenAI)

---

## Prerequisitos

| Herramienta | Versión mínima |
|-------------|----------------|
| Python      | 3.11+          |
| pip         | 23+            |

---

## Setup inicial

```bash
# 1. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install fastapi "uvicorn[standard]" sqlmodel lxml pydantic-settings python-multipart httpx
pip freeze > requirements.txt    # solo la primera vez

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu proveedor LLM (ollama | azure)
```

---

## Variables de entorno (`.env`)

| Variable                  | Default                         | Descripción                       |
|---------------------------|---------------------------------|-----------------------------------|
| `DATABASE_URL`            | `sqlite:///../data/payslips.db` | Ruta a la base de datos SQLite    |
| `UPLOADS_DIR`             | `../uploads`                    | Carpeta donde se guardan PDFs/XML |
| `LLM_PROVIDER`            | `ollama`                        | `ollama` o `azure`                |
| `OLLAMA_BASE_URL`         | `http://localhost:11434`        | Endpoint del daemon Ollama        |
| `OLLAMA_MODEL`            | `qwen2.5:7b-instruct`           | Modelo a usar                     |
| `AZURE_OPENAI_ENDPOINT`   | _(vacío)_                       | Solo si `LLM_PROVIDER=azure`      |
| `AZURE_OPENAI_KEY`        | _(vacío)_                       | Solo si `LLM_PROVIDER=azure`      |
| `AZURE_OPENAI_DEPLOYMENT` | _(vacío)_                       | Solo si `LLM_PROVIDER=azure`      |
| `CORS_ORIGINS`            | `["http://localhost:5173"]`     | Orígenes permitidos por CORS      |

---

## Correr en desarrollo

```bash
# Asegúrate de tener el venv activo
source .venv/bin/activate

uvicorn app.main:app --reload --port 8000
```

La API estará disponible en `http://localhost:8000`.  
Documentación interactiva: `http://localhost:8000/docs`

---

## Verificar que todo funciona

```bash
# Health check
curl http://localhost:8000/health
# Esperado: {"status":"ok","llm_provider":"ollama"}

# Ping al LLM (requiere Ollama corriendo o Azure configurado)
curl http://localhost:8000/llm/ping
# Esperado: {"llm_response": {"ok": true}}
```

---

## Estructura de `app/`

```text
app/
├── __init__.py
├── main.py        # FastAPI entrypoint, CORS, startup
├── config.py      # Settings via pydantic-settings
├── db.py          # Engine, sesión, init_db(), vista `periods`
├── models/        # SQLModel tables (Payslip, LineItem)
├── schemas/       # Pydantic DTOs de request/response
├── services/      # parser XML, llm_client, aggregator
└── routers/       # Rutas: upload, payslips, summary, llm_test
```

---

## Correr tests

```bash
pytest tests/ -v
```

> Los tests que requieren DB usan una base SQLite en memoria — no necesitas `.env` para correrlos.
