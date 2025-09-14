import os
import json
import httpx
from ..settings import settings

SYSTEM_PROMPT = """あなたは日本語のビジネス文書校正アシスタントです。
- 社外向けの丁寧で明瞭な文章に整えます。
- 意味は変えず、冗長表現を簡潔に、二重敬語を避けます。
- 出力は JSON で返してください: {"revised": "...", "reasons": ["...","..."]}"""

async def proofread_with_llm(text: str, tone: str | None, style: str | None) -> dict:
    """OpenAI を呼び出して校正結果を返す（モック可）"""
    if settings.MOCK_OPENAI:
        # モック：最小確認用。行頭に【校正】を付けるだけのダミー
        revised = f"【校正】{text}".strip()
        return {"revised": revised, "reasons": ["mock: format only"]}

    headers = {
        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": settings.OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"トーン:{tone}\nスタイル:{style}\n---\n{text}"},
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]

    # 返答は JSON テキスト想定。壊れても動くようにフォールバック
    try:
        data = json.loads(content)
    except Exception:
        data = {"revised": content, "reasons": []}
    return data
