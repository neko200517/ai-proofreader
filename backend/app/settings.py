import os

from dotenv import load_dotenv

# ローカル開発時だけ .env を読み込み（本番はSSMなど）
load_dotenv(override=False)


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_API_KEY_SSM: str = os.getenv(
        "OPENAI_API_KEY_SSM", "/proofread/openai_api_key"
    )
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    MOCK_OPENAI: bool = os.getenv("MOCK_OPENAI", "true").lower() == "true"
    MAX_INPUT_CHARS_FREE: int = int(os.getenv("MAX_INPUT_CHARS_FREE", "1200"))


settings = Settings()

# --- 追加：OPENAI_API_KEY が無ければ SSM から取得してキャッシュ ---
if settings.OPENAI_API_KEY is None:
    try:
        import boto3

        ssm = boto3.client("ssm")
        resp = ssm.get_parameter(Name=settings.OPENAI_API_KEY_SSM, WithDecryption=True)
        settings.OPENAI_API_KEY = resp["Parameter"]["Value"]
    except Exception:
        # 失敗しても例外は投げず、呼び出し側が has_key=False をログで検知できるようにする
        pass
