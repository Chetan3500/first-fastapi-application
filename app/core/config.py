# Handles environment variables and configuration

from pydantic import BaseSetting
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSetting):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/fastapi_db")
    PROJECT_NAME: str = "FastAPI PostgreSQL CRUD"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()