import asyncio
import logging


from scrap import Scrapper
from utils import Downloader
from orm import DB

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def initial():
    await DB.create_tables()
    scrapper = Scrapper('01.01.2023')
    scrapper.load_bulletins()
    return scrapper


async def loading():
    scrapper = await initial()
    dl = Downloader(source=scrapper.bulletins)
    await dl.loading()


async def print_all() -> None:
    res = await DB.get_all()
    for item in res:
        print(item)


asyncio.run(loading())
# asyncio.run(print_all())



