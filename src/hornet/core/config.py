from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HORNET_", extra="ignore")

    host: str = "0.0.0.0"
    port: int = 8000
    database_url: str = "postgresql+psycopg://hornet:hornet@localhost:5432/hornet"
    redis_url: str = "redis://localhost:6379/0"
    rental_stream: str = "hornet.rentals"
    log_file: str = "logs/hornet.log"
    log_level: str = "INFO"

@lru_cache
def get_settings() -> Settings:
    return Settings()
