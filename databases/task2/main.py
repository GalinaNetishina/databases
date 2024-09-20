import logging
import datetime as dt
import os

from scrap import Scrapper
from utils import objects_from_file, download_parallel
from orm import AsyncORM

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")


async def initial_base() -> None:
    await AsyncORM.create_tables()

    scrapper.default_date = dt.datetime.strptime('01.01.2023', '%d.%m.%Y').date()

    async for dump in scrapper.bulletins:
        filename = f'{dump.date}.xls'
        await dump.download_file(filename)
        await AsyncORM.insert(objects_from_file(filename))
        os.remove('temp/' + filename)
        logging.debug('part is loaded')


async def print_all() -> None:
    await AsyncORM.create_tables()
    res = await AsyncORM.show()
    # for (i, item), _ in zip(enumerate(res.all(), start=1), range(30)): # вывод порции
    for i, item in enumerate(res.all(), start=1):
        print(item)
    print(f'total: {i} items')
    # print(*(item for _, item in enumerate(res.all()) if item[0].exchange_product_name.startswith('Топливо')),
    #       sep='\n')


# asyncio.run(initial_base())

# asyncio.run(print_all())\

scrapper = Scrapper('01.09.2024')
scrapper.load_bulletins()
for *portion_bulletins, _ in zip(scrapper.bulletins, range(10)):
    download_parallel(portion_bulletins)

