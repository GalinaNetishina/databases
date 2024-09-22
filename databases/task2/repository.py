from typing import Iterator

from sqlalchemy import select

from database import async_session_maker
from models import Item
from schema import ItemDTO


class Repository:
    @classmethod
    async def add_one(cls, data: Item) -> int:
        async with async_session_maker() as session:
            item = data
            session.add(item)
            await session.flush()
            await session.commit()
            return item.id

    @classmethod
    async def add_many(cls, data) -> None:
        async with async_session_maker() as session:
            session.add_all(data)
            await session.commit()

    @classmethod
    async def get_one(cls, id: int) -> ItemDTO:
        async with async_session_maker() as session:
            query = select(Item).filter_by(id=id)
            res = await session.execute(query)
            res_dto = ItemDTO.model_validate(res.scalars().one_or_none(), from_attributes=True)
            return res_dto

    @classmethod
    async def generator(cls) -> Iterator[ItemDTO]:
        async with async_session_maker() as session:
            query = select(Item).order_by(Item.date)
            res = await session.execute(query)
            return map(lambda x: ItemDTO.model_validate(x, from_attributes=True), res.scalars().all())
