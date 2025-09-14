import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .handlers.debug import router as debug_router
from .handlers.proofread import router as proofread_router

app = FastAPI()

# デプロイ後に CloudFront ドメインを追加予定。MVPではローカル許可でOK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番は後で絞る
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(proofread_router, prefix="/api")


app.include_router(debug_router, prefix="/debug")


@app.get("/health")
def health():
    return {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL"),
        "MOCK_OPENAI": os.getenv("MOCK_OPENAI"),
        "MAX_INPUT_CHARS_FREE": os.getenv("MAX_INPUT_CHARS_FREE"),
        "ok": True,
    }
