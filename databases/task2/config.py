from dotenv import load_dotenv
import os


class Settings:
    def __init__(self):
        load_dotenv()

        self.DB_NAME: str = os.environ.get('DB_NAME')
        self.DB_HOST: str = os.environ.get('DB_HOST')
        self.DB_PORT: str | int = os.environ.get('DB_PORT')
        self.DB_USER: str = os.environ.get('DB_USER')
        self.DB_PASS: str = os.environ.get('DB_PASS')
        self.DEBUG: bool = False

    @property
    def DSN_postgresql_psycopg(self) -> str:
        return (f'postgresql+psycopg2://'
                f'{self.DB_USER}:'
                f'{self.DB_PASS}'
                f'@{self.DB_HOST}:'
                f'{self.DB_PORT}/'
                f'{self.DB_NAME}')

    @property
    def DSN_postgresql_asyncpg(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:'
                f'{self.DB_PASS}'
                f'@{self.DB_HOST}:'
                f'{self.DB_PORT}/'
                f'{self.DB_NAME}')


settings = Settings()
