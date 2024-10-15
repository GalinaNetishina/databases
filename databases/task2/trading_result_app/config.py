from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    SMTP_USER: str
    SMTP_PASSWORD: str
    REDIS_HOST: str
    REDIS_PORT: int
    FRONTEND_HOST: str
    FRONTEND_PORT: int

    model_config = SettingsConfigDict(
        env_file=os.path.join(Path.cwd().parent, ".env")
    )

    @property
    def DSN_postgresql_psycopg(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    @property
    def DSN_postgresql_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )


settings = Settings()
