# app/config.py
from __future__ import annotations
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError

class Settings(BaseSettings):
    # obligatorias (las das por compose/.env)
    DATABASE_URL: str
    INSTANCE: str
    ENV: str
    API_AUDIENCE: str
    REDIS_URL: str

    # claves: por valor (PEM) o por archivo (ruta)
    JWT_PUBLIC_KEY: str = ""                      # PEM en texto (multilínea OK)
    JWT_PUBLIC_KEY_FILE: Optional[str] = None     # ruta opcional

    JWT_PRIVATE_KEY: str = ""                     # SOLO dev/demo (para firmar)
    JWT_PRIVATE_KEY_FILE: Optional[str] = None    # ruta opcional

    # emisor demo
    JWT_ISSUER: str = "demo-issuer"
    JWT_TTL_MIN: int = 10
    ENABLE_DEMO_TOKEN: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()

# ---- cargar desde archivo si corresponde ----
def _load_file(path: Optional[str]) -> str:
    return Path(path).read_text(encoding="utf-8") if path else ""

if not settings.JWT_PUBLIC_KEY and settings.JWT_PUBLIC_KEY_FILE:
    settings.JWT_PUBLIC_KEY = _load_file(settings.JWT_PUBLIC_KEY_FILE)

if not settings.JWT_PRIVATE_KEY and settings.JWT_PRIVATE_KEY_FILE:
    settings.JWT_PRIVATE_KEY = _load_file(settings.JWT_PRIVATE_KEY_FILE)

# ---- validaciones de coherencia ----
if not settings.JWT_PUBLIC_KEY:
    raise RuntimeError("JWT_PUBLIC_KEY no está presente (ni archivo ni valor).")

if settings.ENABLE_DEMO_TOKEN and not settings.JWT_PRIVATE_KEY:
    raise RuntimeError(
        "ENABLE_DEMO_TOKEN=true requiere JWT_PRIVATE_KEY (o *_FILE) para firmar tokens."
    )
