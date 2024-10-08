import asyncio
import logging
import time

from fastapi import FastAPI

from utils import Downloader
from database import create_tables
from router import router as root

from repository import Repository as Repo

logging.basicConfig(level=logging.INFO, format=" %(message)s")


async def full_load(after: str = "01.01.2024") -> None:
    await create_tables()
    dl = Downloader(after, Repo.add_many)

    start = time.time()
    await dl.download_1()
    stop = time.time()
    logging.info(f"load to DB in 2fases time: - {round(stop - start, 2)}s")

    start = time.time()
    await dl.download_2()
    stop = time.time()
    logging.info(f"load to DB paralel time: - {round(stop - start, 2)}s")


app = FastAPI()
app.include_router(root)


if __name__ == "__main__":
    asyncio.run(full_load())
