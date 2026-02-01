from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 5
    ALLOWD_FILE_TYPE: list = [".pdf"]

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 65

    DATABASE_URL: Optional[str] = None

    PINECONE_API_KEY: Optional[str] = None
    PINCONE_ENV: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
