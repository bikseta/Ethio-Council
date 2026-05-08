from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://ecfe_user:ecfe_pass@db:5432/ecfe_db"
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    app_name: str = "ECFE Analytics Service"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
