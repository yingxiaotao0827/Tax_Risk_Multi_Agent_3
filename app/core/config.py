from functools import lru_cache
import os
from pathlib import Path

try:
    from pydantic import Field
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ModuleNotFoundError:  # pragma: no cover - local bootstrap fallback
    Field = None
    BaseSettings = object
    SettingsConfigDict = None


class Settings(BaseSettings):
    if SettingsConfigDict:
        model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = os.getenv("APP_NAME", "tax-risk-ai")
    environment: str = os.getenv("ENVIRONMENT", "local")
    data_dir: Path = Path(os.getenv("DATA_DIR", "tax_risk_ai/data"))
    sqlite_path: Path = Path(os.getenv("SQLITE_PATH", "tax_risk_ai/data/tax_demo.db"))

    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_model: str = os.getenv("LLM_MODEL", "Qwen2.5-14B-Instruct")
    llm_base_url: str = os.getenv("LLM_BASE_URL", "http://localhost:8001/v1")
    llm_api_key: str = os.getenv("LLM_API_KEY", "local")

    milvus_uri: str = os.getenv("MILVUS_URI", "http://localhost:19530")
    milvus_collection: str = os.getenv("MILVUS_COLLECTION", "tax_rules_2025")
    embedding_model: str = os.getenv(
        "EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )

    max_tool_calls: int = int(os.getenv("MAX_TOOL_CALLS", "8"))
    min_supervisor_score: float = float(os.getenv("MIN_SUPERVISOR_SCORE", "0.72"))
    min_report_confidence: float = float(os.getenv("MIN_REPORT_CONFIDENCE", "0.68"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
