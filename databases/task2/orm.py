from sqlalchemy import select

from database import async_engine, async_session_maker
from models import *


class DB:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def reflect_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.reflect)

    @staticmethod
    async def get_all():
        async with async_session_maker() as session:
            query = select(Item).order_by(Item.date)
            res = await session.execute(query)
            return res.scalars().all()
