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
# macOS / Linux: usa python3 explícitamente (el comando "python" puede no existir)
python3 -m venv .venv
# Windows: python -m venv .venv

source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env con tu proveedor LLM (ollama | azure)
```

---

## Dependencias

| Paquete              | Propósito                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `fastapi`            | Framework web asíncrono para construir la API REST                        |
| `uvicorn[standard]`  | Servidor ASGI que corre la app FastAPI; `[standard]` incluye hot reload   |
| `sqlmodel`           | ORM que combina SQLAlchemy + Pydantic; define tablas y valida datos       |
| `pydantic-settings`  | Carga y valida variables de entorno desde `.env` en `config.py`           |
| `python-multipart`   | Habilita recepción de archivos (`multipart/form-data`) en FastAPI         |
| `httpx`              | Cliente HTTP asíncrono para llamar a la API de Ollama o Azure OpenAI      |

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
