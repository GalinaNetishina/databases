# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from config import settings


async_engine = create_async_engine(
    url=settings.DSN_postgresql_asyncpg,
    echo=settings.DEBUG,
    future=True,
    pool_size=50,
    max_overflow=100
)


async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)



