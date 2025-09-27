# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # URL de la DB
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/recipes"

    # nombre de la instancia (para /health)
    INSTANCE: str = os.getenv("INSTANCE", "api")

    # ambiente (dev/prod/test)
    ENV: str = os.getenv("ENV", "dev")

    class Config:
        env_file = ".env"

# instancia global
settings = Settings()
