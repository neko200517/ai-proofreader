from fastapi import FastAPI
from .handlers.proofread import router as proofread_router

app = FastAPI()
app.include_router(proofread_router, prefix="/api")

@app.get("/health")
def health():
    return {"ok": True}
