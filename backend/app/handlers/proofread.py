from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ..security.sanitize import mask_pii
from ..services.llm import proofread_with_llm
from ..settings import settings

router = APIRouter()

ALLOWED_TONES = ["社外-丁寧", "社外-強フォーマル", "社内-カジュアル"]
ALLOWED_STYLES = ["依頼", "連絡", "報告", "謝罪"]


class ProofreadReq(BaseModel):
    text: str = Field(..., min_length=1, max_length=50_000)
    tone: str | None = Field(default="社外-丁寧")
    style: str | None = Field(default="依頼")


class ProofreadRes(BaseModel):
    revised: str
    reasons: list[str] = []


@router.post("/proofread", response_model=ProofreadRes)
async def proofread(req: ProofreadReq):
    # 入力上限（無料の想定上限）。本格的なプラン判定は後章でサービス層に寄せる
    if len(req.text) > settings.MAX_INPUT_CHARS_FREE:
        raise HTTPException(
            status_code=413, detail="入力文字数の上限を超えています（開発中の暫定制限）"
        )

    # トーン/スタイルは未知値も許容したいが、MVPでは簡単なホワイトリストに
    tone = req.tone if req.tone in ALLOWED_TONES else "社外-丁寧"
    style = req.style if req.style in ALLOWED_STYLES else "依頼"

    masked = mask_pii(req.text)
    data = await proofread_with_llm(masked, tone, style)

    # 最低限の整形（空は許容しない）
    revised = (data.get("revised") or "").strip()
    reasons = data.get("reasons") or []
    if not revised:
        raise HTTPException(status_code=502, detail="校正結果が空でした")

    return ProofreadRes(revised=revised, reasons=reasons)
