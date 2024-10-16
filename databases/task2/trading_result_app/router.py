import asyncio
from datetime import datetime
from functools import partial
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache

from schema import ItemDTO, TradingDay
from database import get_async_session
from repository import Repository as Repo

from var2 import Downloader

router = APIRouter()

def get_pag_params(limit: int = 10, skip: int = 0):
        return {
                'limit': limit,
                'skip': skip
                }



@router.get("/get_trading_results/", tags=["Список последних торгов"])
@cache(expire=3600)
async def get_trading_results(
    pag_params = Depends(get_pag_params),
    session: AsyncSession = Depends(get_async_session),
    exchange_product_id=None,
    delivery_basis_id=None,
    delivery_type_id=None,
) -> list[ItemDTO]:
    res = await Repo.get_last(session, **pag_params)
    return res


@router.get("/item/{id}", tags=["Результаты торгов за период"])
@cache(expire=3600)
async def get_dynamics(
    session: AsyncSession = Depends(get_async_session),
) -> list[ItemDTO]:
    res = await Repo.get_lot(session)
    return res


@router.get("/last_trading_dates/{count}", tags=["Даты последних торгов"])
@cache(expire=3600)
async def get_last_trading_dates(
    session: AsyncSession = Depends(get_async_session), count: int = 10
) -> list[TradingDay]:
    res = await Repo.get_last_trading_dates(session, count)
    return res

@router.get("/load/", tags=["Загрузка данных"])
async def full_load(
     session: AsyncSession = Depends(get_async_session)
) -> None:
    # after = await Repo.get_last_trading_dates(1)
    # if datetime.today().date() - after[0].date > timedelta(days=3):
    #     after = after[0].date.strftime("%d.%m.%Y")
    dl = Downloader('01.09.2024', partial(Repo.add_many, session))
    asyncio.get_event_loop().run_in_executor(None, dl.download)
    return {"status": "OK",
            "message": "Loading is started"}
