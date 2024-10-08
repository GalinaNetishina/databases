import asyncio
import logging

from fastapi import FastAPI

from scrap import Scrapper
from utils import Downloader
from database import create_tables
from repository import Repository as Repo
from router import router as root

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def full_load(after: str = '01.09.2024') -> None:
    await create_tables()
    scrapper = Scrapper(after)
    scrapper.load_bulletins()
    dl = Downloader(source=scrapper.bulletins)
    while part := await dl.next_portion():
        while dl.output:
            data = dl.output.pop()
            await Repo.add_many(data)
        logging.info('portion in DB')
    logging.info('loading to DB completed')


app = FastAPI()
app.include_router(root)


if __name__ == "__main__":
    asyncio.run(full_load())
