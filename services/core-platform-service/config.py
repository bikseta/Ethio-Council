from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/ethio_council"
    secret_key: str = "ethio-council-dev-secret-key-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours

    # CORS
    allowed_origins: str = "http://localhost:3000"
    frontend_url: str = "http://localhost:3000"

    # Email
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "noreply@ecfe.et"
    smtp_password: str = ""

    # Service URLs
    gis_service_url: str = "http://gis-service:8000"
    analytics_service_url: str = "http://analytics-service:8000"
    crisis_service_url: str = "http://crisis-service:8000"

    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
