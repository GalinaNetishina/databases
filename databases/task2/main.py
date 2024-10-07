import asyncio
import logging
import time

from fastapi import FastAPI

from scrap import Scrapper
from utils import Downloader
from database import create_tables
from router import router as root

from repository import Repository as Repo

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def full_load(after: str = "01.01.2023") -> None:
    await create_tables()
    scrapper = Scrapper(after)
    scrapper.load_bulletins()
    dl = Downloader(source=scrapper.bulletins)
    await dl.download()
    start = time.time()

    while part := await dl.next_portion():
        while dl.output:
            data = dl.output.pop()
            await Repo.add_many(data)
    stop = time.time()
    logging.info(f"load to DB time: - {round(stop - start, 2)}s")
    #     logging.info('portion in DB')
    # logging.info('loading to DB completed')


app = FastAPI()
app.include_router(root)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(full_load())
    stop = time.time()
    logging.info(f"total time: - {round(stop - start, 2)}s")
