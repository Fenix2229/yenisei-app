from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_name: str = "История реки Енисей"
    app_version: str = "1.0.0"
    database_url: str = "sqlite:///./yenisei.db"
    cors_origins: list = [
        "http://localhost:5173", 
        "http://localhost:3000",
        "https://yenisei-backend.onrender.com",
        "https://g917904o.beget.tech"
    ]
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()