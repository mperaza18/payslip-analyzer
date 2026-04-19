# Backend — Payslip Analyzer

FastAPI + SQLModel + LLM client (Ollama / Azure OpenAI).

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # ajusta variables
uvicorn app.main:app --reload --port 8000
```
