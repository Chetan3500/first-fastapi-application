"""Handles environment variables and configuration"""

import os
from pydantic.v1 import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Base Settings"""

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://username:password@localhost:5432/fastapi_db"
    )
    PROJECT_NAME: str = "FastAPI PostgreSQL CRUD"
    API_V1_STR: str = "/api/v1"

    class Config:
        """Environment configure"""

        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
