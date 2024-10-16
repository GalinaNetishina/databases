from datetime import date
from typing import List

from sqlalchemy import desc, select
from sqlalchemy.orm import load_only


from models import Item
from schema import ItemDTO, TradingDay


class Repository:
    @classmethod
    async def add_one(cls, session, data: Item) -> int:
        
            item = data
            session.add(item)
            await session.flush()
            await session.commit()
            return item.id

    @classmethod
    async def add_many(cls, session, data) -> None:
       
            session.bulk_save_objects(data)
            await session.commit()

    @classmethod
    async def get_one(cls, session, id: int) -> ItemDTO:
        
            query = select(Item).filter_by(id=id)
            res = await session.execute(query)
            res_dto = ItemDTO.model_validate(
                res.scalars().one_or_none(), from_attributes=True
            )
            return res_dto

    @classmethod
    async def get_last(cls, session, limit, skip) -> List[ItemDTO]:
        
            last_date = date(2024, 10, 14)
            
            query = (
                select(Item)
                .where(Item.date==last_date)
                .limit(limit)
                .offset(skip)
            )
            # match(filters):
            #         case {'exchange_product_id': value}:
            #             query.where(Item.exchange_product_id == value)
            #             print('filter1')
            #         case {'delivery_basis_id': value}:
            #             query.where(Item.delivery_basis_id == value)
            #             print('filter2')
            #         case {'delivery_type_id': value}:
            #             query.where(Item.delivery_type_id == value)
            #             print('filter3')
            # print(query)
            res = await session.execute(query)
            return list(map(
                lambda x: ItemDTO.model_validate(x, from_attributes=True),
                res.scalars().all(),
            ))

    @classmethod
    async def get_last_trading_dates(cls, session, count: int) -> list[TradingDay]:
      
            query = (
                select(Item)
                .order_by(desc(Item.date))
                .options(load_only(Item.date))
                .distinct(Item.date)
                .limit(count)
            )
            
            res = await session.execute(query)
            return list(
                map(
                    lambda x: TradingDay.model_validate(x, from_attributes=True),
                    res.scalars().all(),
                )
            )
