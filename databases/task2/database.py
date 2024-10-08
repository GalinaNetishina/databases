from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine

from config import settings
from models import Base


async_engine = create_async_engine(
    url=settings.DSN_postgresql_asyncpg,
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


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def reflect_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.reflect)
