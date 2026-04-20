# Phase 1 — Backend Setup

Files created to implement the FastAPI foundation (Paso 2 of Phase 1).

---

## `app/config.py`

Settings via pydantic-settings — reads all variables from `backend/.env`.

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str = "sqlite:///../data/payslips.db"
    UPLOADS_DIR: str = "../uploads"

    LLM_PROVIDER: str = "ollama"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b-instruct"

    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT: str = ""

    CORS_ORIGINS: List[str] = ["http://localhost:5173"]


settings = Settings()
```

---

## `app/db.py`

SQLModel engine, `init_db()` to create all tables on startup, and `get_session()` for dependency injection in routers.

```python
from sqlmodel import SQLModel, create_engine, Session
from .config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

---

## `app/services/llm_client.py`

Abstract `LLMClient` interface with two concrete implementations (`OllamaClient`, `AzureOpenAIClient`) and a factory `get_llm()` that selects the provider based on `LLM_PROVIDER`.

```python
from abc import ABC, abstractmethod
import httpx
from ..config import settings


class LLMClient(ABC):
    @abstractmethod
    async def chat(self, prompt: str) -> dict:
        ...


class OllamaClient(LLMClient):
    async def chat(self, prompt: str) -> dict:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                f"{settings.OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": settings.OLLAMA_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                },
            )
            response.raise_for_status()
            return response.json()


class AzureOpenAIClient(LLMClient):
    async def chat(self, prompt: str) -> dict:
        headers = {
            "api-key": settings.AZURE_OPENAI_KEY,
            "Content-Type": "application/json",
        }
        url = (
            f"{settings.AZURE_OPENAI_ENDPOINT}/openai/deployments/"
            f"{settings.AZURE_OPENAI_DEPLOYMENT}/chat/completions?api-version=2024-02-01"
        )
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                url,
                headers=headers,
                json={
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            response.raise_for_status()
            return response.json()


def get_llm() -> LLMClient:
    if settings.LLM_PROVIDER == "azure":
        return AzureOpenAIClient()
    return OllamaClient()
```

---

## `app/routers/llm_test.py`

`GET /llm/ping` — sends a minimal prompt to the configured LLM and returns the raw response. Used to verify the LLM is reachable.

```python
from fastapi import APIRouter
from ..services.llm_client import get_llm

router = APIRouter(prefix="/llm", tags=["llm"])


@router.get("/ping")
async def ping_llm():
    client = get_llm()
    result = await client.chat("Respond with valid JSON: {\"ok\": true}")
    return {"llm_response": result}
```

---

## `app/main.py`

FastAPI entrypoint — configures CORS, registers the startup hook (`init_db`), mounts routers, and exposes `/health`.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .db import init_db
from .routers import llm_test

app = FastAPI(title="Payslip Analyzer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


app.include_router(llm_test.router)


@app.get("/health")
def health():
    return {"status": "ok", "llm_provider": settings.LLM_PROVIDER}
```

---

## Verification

```bash
# Start the server (from backend/ with venv active)
uvicorn app.main:app --reload --port 8000

# Health check
curl http://localhost:8000/health
# {"status":"ok","llm_provider":"ollama"}

# LLM ping (requires Ollama running or Azure configured)
curl http://localhost:8000/llm/ping
# {"llm_response": {"ok": true}}
```
