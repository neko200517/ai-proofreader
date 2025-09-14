from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .handlers.proofread import router as proofread_router

app = FastAPI()

# --- CORS 対応を追加 ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # すべてのオリジンを許可（本番では絞る）
    allow_credentials=True,
    allow_methods=["*"], # GET, POST など全メソッド許可
    allow_headers=["*"], # すべてのヘッダーを許可
)

# --- ルーター登録 ---
app.include_router(proofread_router, prefix="/api")

@app.get("/health")
def health():
    return {"ok": True}
