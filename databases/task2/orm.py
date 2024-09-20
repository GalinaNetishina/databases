from sqlalchemy import select

from databases.task2.database import async_engine, async_session_maker
from databases.task2.models import *


class AsyncORM:
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.reflect)

    @staticmethod
    async def insert(args):
        async with async_session_maker() as session:
            session.add_all(args)
            await session.commit()

    @staticmethod
    async def show():
        async with async_session_maker() as session:
            query = select(Item)
            res = await session.execute(query)
            return res.scalars()
