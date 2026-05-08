from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:changeme@localhost:5434/ethio_council"
    allowed_origins: str = "http://localhost:3001"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
