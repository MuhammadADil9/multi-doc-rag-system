from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    MAX_FILE_SIZE_MB: int = 5
    ALLOWD_FILE_TYPE: list = [".pdf"]

    CHUNK_SIZE: int = 512
    CHUNK_OVERLAP: int = 65

    DATABASE_URL: Optional[str] = (
        "postgresql://neondb_owner:npg_EZRsxgM69CeP@ep-shy-band-ahn8iqnb-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )

    PINECONE_API_KEY: Optional[str] = (
        "pcsk_2NiKkS_TmjUzppAk6wDdD394WGhiks6dKzL8Wv35TDrGwyuLs7KuAKRnpsSK4oqLSV6zeF"
    )
    PINCONE_ENV: Optional[str] = "us-east-1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
