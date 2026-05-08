from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://ecfe_user:ecfe_pass@db:5432/ecfe_db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_region: str = "us-east-1"
    aws_endpoint_url: str = "http://localstack:4566"
    s3_bucket_name: str = "ecfe-documents"
    app_name: str = "ECFE GIS Registration Service"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
