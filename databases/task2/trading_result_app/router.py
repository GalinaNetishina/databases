from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from schema import ItemDTO, ItemFull, TradingDay, ItemDateIdFilter, ItemIdFilter
from database import get_async_session
from repository import Repository as Repo


router = APIRouter(prefix="/api")


def get_pag_params(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}


@router.get("/get_trading_results/", tags=["Список последних торгов"])
@cache(expire=3600)
async def get_trading_results(
    pag_params=Depends(get_pag_params),
    filter: ItemIdFilter = FilterDepends(ItemIdFilter),
    session: AsyncSession = Depends(get_async_session),
) -> list[ItemDTO]:
    res = await Repo.get_last(session, filter, **pag_params)
    return res


@router.get("/get_dynamics/", tags=["Список торгов  в диапазоне дат"])
@cache(expire=3600)
async def get_dynamics(
    pag_params=Depends(get_pag_params),
    filter: ItemIdFilter = FilterDepends(ItemDateIdFilter),
    session: AsyncSession = Depends(get_async_session),
) -> list[ItemDTO]:
    res = await Repo.get_many(session, filter, **pag_params)
    return res


@router.get("/item/{id}", tags=["Детали о лоте по id"])
@cache(expire=3600)
async def get_item(
    id: int, session: AsyncSession = Depends(get_async_session)
) -> ItemFull:
    res = await Repo.get_one(session, id)
    return res


@router.get("/last_trading_dates/", tags=["Даты последних торгов"])
@cache(expire=3600)
async def get_last_trading_dates(
    session: AsyncSession = Depends(get_async_session), count: int = 10
) -> list[TradingDay]:
    res = await Repo.get_last_trading_dates(session, count)
    return res
