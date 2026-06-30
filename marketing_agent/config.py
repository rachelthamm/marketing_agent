from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    llm_provider: Literal["anthropic", "gemini", "ollama"] = "ollama"
    anthropic_api_key: str = Field(default="")
    google_api_key: str = Field(default="")
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen3.5:0.8b"

    supabase_url: str = Field(default="")
    supabase_service_key: str = Field(default="")

    postiz_base_url: str = "http://localhost:3000"
    postiz_api_key: str = ""

    n8n_base_url: str = "http://localhost:5678"
    n8n_webhook_secret: str = ""

    log_level: str = "INFO"
    environment: str = "development"


settings = Settings()
