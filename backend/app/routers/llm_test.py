from fastapi import APIRouter
from ..services.llm_client import get_llm

router = APIRouter(prefix="/llm", tags=["llm"])


@router.get("/ping")
async def ping_llm():
    client = get_llm()
    result = await client.chat("Respond with valid JSON: {\"ok\": true}")
    return {"llm_response": result}
