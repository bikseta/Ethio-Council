from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    database_url: str = "postgresql://ecfe_user:ecfe_pass@localhost:5432/ecfe_db"
    secret_key: str = "ecfe-dev-secret-key-2024"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_default_region: str = "us-east-1"
    aws_endpoint_url: Optional[str] = "http://localhost:4566"
    s3_documents_bucket: str = "ecfe-documents"
    frontend_url: str = "http://localhost:3001"

    class Config:
        env_file = ".env"


settings = Settings()
