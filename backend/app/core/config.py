from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Automation System"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "changeme"
    GOOGLE_CLIENT_ID: str 
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str 

    # PostgreSQL
    POSTGRES_URL: str

    class Config:
        env_file = ".env"
        case_sensitive = True

# objects are created at once and reused everywhere. No re-reading the env file again and again.
@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()