# backend/app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Fantacazzate API"
    debug: bool = True
    database_url: str = "sqlite:///./fantacazzate.db"
    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Auth
    secret_key: str = "changeme-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 giorni
    app_password: str = "fantacazzate2026"    # password condivisa

    class Config:
        env_file = ".env"

settings = Settings()