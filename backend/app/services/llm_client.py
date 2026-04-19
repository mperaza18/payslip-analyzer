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
