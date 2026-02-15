import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AEGIS One API"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/postgres"

    # JWT
    JWT_SECRET_KEY: str = "aegis-one-super-secret-key-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Official Domain
    OFFICIAL_EMAIL_DOMAIN: str = "iitmandi.ac.in"

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
