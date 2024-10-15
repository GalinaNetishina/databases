from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from fastapi_pagination import paginate, Page

from schema import ItemDTO, TradingDay
from database import get_async_session
from repository import Repository as Repo

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
