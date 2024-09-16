import asyncio
import logging
import datetime as dt
import os


from databases.task2.scrap import Scrapper
from databases.task2.utils import objects_from_file
from databases.task2.orm import SyncORM


logging.basicConfig(level=logging.info, format="%(asctime)s %(levelname)s %(message)s")

SyncORM.create_tables()


async def initial_base():
    scrap = Scrapper()
    scrap.default_date = dt.datetime.strptime('01.01.2024', '%d.%m.%Y').date()

    async for dump in scrap.bulletins:
        filename = f'{dump.date}.xls'
        await dump.download_file(filename)
        SyncORM.insert(*(item for item in objects_from_file(date=dump.date)))
        os.remove('temp/'+filename)
        logging.debug('part is loaded')


#SyncORM.show()
asyncio.run(initial_base())



