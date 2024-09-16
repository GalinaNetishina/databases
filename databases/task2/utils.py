import logging
from typing import NamedTuple, Iterable
from datetime import datetime as dt
import requests, xlrd

from databases.task2.database import session_factory
from databases.task2.models import Item
from databases.task2.scrap import Scrapper


class RawItem(NamedTuple):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis: str
    volume: int
    total: int
    count: int
    date: dt

    def to_Item(self):
        return Item(
            exchange_product_id=self.exchange_product_id,
            exchange_product_name=self.exchange_product_name,
            oil_id=self.exchange_product_id[:4],
            delivery_basis_id=self.exchange_product_id[4:7],
            delivery_basis_name=self.delivery_basis,
            delivery_type_id=self.exchange_product_id[-1],
            volume=self.volume,
            total=self.total,
            count=self.count,
            date=self.date
        )


def download_file(rel_url):
    base_url = 'https://spimex.com/'
    url = base_url + rel_url
    response = requests.get(url)
    if response.status_code == 200:
        with open('temp/data.xls', 'wb') as file:
            file.write(response.content)
        logging.debug('file downloaded successfully')
    else:
        logging.error('Failed to download file')


def objects_from_file(file, date) -> Iterable[Item]:
    source = xlrd.open_workbook(file)
    sheet = source.sheet_by_index(0)
    for i in range(8, sheet.nrows - 2):
        _, id, name, basis, *tail = (sheet[i][j].value for j in range(sheet.ncols))
        print(_, id, name, basis, *(map(repr, tail)))
        volume, total, count = tail[0], tail[1], tail[5]
        if not volume or not total or not count:
            continue
        if '-' in (volume, total, count):
            continue
        try:
            yield RawItem(id, name.split(',')[0], basis, int(volume), int(total), int(count), date).to_Item()
        except ValueError:
            yield RawItem(id, name.split(',')[0], basis, int(float(volume)*1000), int(float(total)*1000), int(float(count)*1000), date).to_Item()
