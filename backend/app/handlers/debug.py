from fastapi import APIRouter

from ..settings import settings

router = APIRouter()


@router.get("/env")
def env_probe():
    return {
        "mock_openai": settings.MOCK_OPENAI,
        "model": settings.OPENAI_MODEL,
        "has_openai_key": bool(settings.OPENAI_API_KEY),  # 値は返さない
        "input_limit": settings.MAX_INPUT_CHARS_FREE,
    }
