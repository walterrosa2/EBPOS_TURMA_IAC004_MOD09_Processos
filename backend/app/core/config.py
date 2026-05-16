import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Força o .env a SEMPRE sobrescrever variáveis de ambiente do sistema (Windows/Linux)
# Sem override=True, variáveis definidas via `setx` no Windows teriam prioridade.
load_dotenv(override=True)

class Settings(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "QDT Processos Contabeis API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./data/qdt_processos.db")
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY", None)
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o")
    openai_timeout_seconds: int = int(os.getenv("OPENAI_TIMEOUT_SECONDS", "60"))
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", env_file_encoding="utf-8")

settings = Settings()
