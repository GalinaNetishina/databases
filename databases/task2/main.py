import asyncio
import logging
import datetime as dt
import os

from databases.task2.scrap import scrapper
from databases.task2.utils import objects_from_file
from databases.task2.orm import AsyncORM

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


async def initial_base() -> None:
    await AsyncORM.create_tables()
    os.makedirs('temp', exist_ok=True)
    scrapper.default_date = dt.datetime.strptime('01.01.2024', '%d.%m.%Y').date()
    async for dump in scrapper.bulletins:
        filename = f'{dump.date}.xls'
        await dump.download_file(filename)
        await AsyncORM.insert(objects_from_file(filename))
        os.remove('temp/' + filename)
        logging.debug('part is loaded')


async def print_all() -> None:
    res = await AsyncORM.show()
    # for (i, item), _ in zip(enumerate(res.all(), start=1), range(30)): # вывод порции
    for i, item in enumerate(res.all(), start=1):
        print(item[0])
    print(f'total: {i} items')
    # print(*(item[0] for _, item in enumerate(res.all()) if item[0].exchange_product_name.startswith('Топливо')),
    #       sep='\n')


asyncio.run(initial_base())
asyncio.run(print_all())
