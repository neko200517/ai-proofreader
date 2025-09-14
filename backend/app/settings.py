import os

from dotenv import load_dotenv

# ローカル開発時だけ .env を読み込み（本番はSSMなど）
load_dotenv(override=False)


class Settings:
    OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    MOCK_OPENAI: bool = os.getenv("MOCK_OPENAI", "true").lower() == "true"
    MAX_INPUT_CHARS_FREE: int = int(os.getenv("MAX_INPUT_CHARS_FREE", "1200"))


settings = Settings()
