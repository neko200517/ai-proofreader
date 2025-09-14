import re

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"\b0\d{1,4}-\d{1,4}-\d{3,4}\b")


def mask_pii(text: str) -> str:
    text = EMAIL_RE.sub("[メールアドレス]", text)
    text = PHONE_RE.sub("[電話番号]", text)
    return text
