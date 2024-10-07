from environs import Env


class Settings:
    def __init__(self):
        env = Env()
        env.read_env()
        self.DB_NAME: str = env("DB_NAME")
        self.DB_HOST: str = env("DB_HOST")
        self.DB_PORT: int = env("DB_PORT")
        self.DB_USER: str = env("DB_USER")
        self.DB_PASS: str = env("DB_PASS")

    @property
    def DSN_postgresql_psycopg(self):
        return (
            f"postgresql+psycopg2://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    @property
    def DSN_postgresql_asyncpg(self):
        return (
            f"postgresql+asyncpg://"
            f"{self.DB_USER}:"
            f"{self.DB_PASS}"
            f"@{self.DB_HOST}:"
            f"{self.DB_PORT}/"
            f"{self.DB_NAME}"
        )

    @property
    def sqlite_engine(self):
        return f"sqlite:///{self.DB_NAME}.db"


settings = Settings()
