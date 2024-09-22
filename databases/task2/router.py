from fastapi import APIRouter

from schema import ItemDTO
from repository import Repository  as Repo
router = APIRouter()


@router.get('/show/{count}', tags=['Результаты торгов'])
async def show(count: int = 10) -> list[ItemDTO]:
    generator = await Repo.generator()
    return [next(generator) for _ in range(count)]


@router.get('/item/{id}', tags=['Лот'])
async def get_item(id: int) -> ItemDTO:
    res = await Repo.get_one(id)
    return res
