from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:changeme@localhost:5434/ethio_council"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_default_region: str = "us-east-1"
    aws_endpoint_url: Optional[str] = "http://localhost:4566"
    frontend_url: str = "http://localhost:3001"
    allowed_origins: str = "http://localhost:3001"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
