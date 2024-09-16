import logging
import datetime as dt
from databases.task2.scrap import Scrapper
from databases.task2.utils import download_file, objects_from_file
from databases.task2.orm import SyncORM


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

SyncORM.create_tables()

scrap = Scrapper()
scrap.default_date = dt.datetime.strptime('01.01.2024', '%d.%m.%Y').date()
for dump in scrap.bulletins:
    download_file(dump.url)
    SyncORM.insert(*(item for item in objects_from_file('temp/data.xls', date=dump.date)))
    logging.debug('part is loaded')
SyncORM.show()



