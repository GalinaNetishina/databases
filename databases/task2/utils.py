import logging
from typing import NamedTuple, AsyncGenerator
from datetime import datetime as dt
import xlrd

from databases.task2.models import Item


class RawItem(NamedTuple):
    exchange_product_id: str
    exchange_product_name: str
    delivery_basis: str
    volume: int
    total: int
    count: int
    date: dt.date

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


def objects_from_file(filename) -> AsyncGenerator[Item, None]:
    """generates sequence of Item from .xls file"""
    try:
        source = xlrd.open_workbook(f'temp/{filename}')
        sheet = source.sheet_by_index(0)
        for i in range(8, sheet.nrows - 2):
            _, id, name, basis, *tail = (sheet[i][j].value for j in range(sheet.ncols))
            volume, total, count = tail[0], tail[1], tail[5]
            date = dt.strptime(filename[:-4], '%Y-%m-%d').date()
            if not volume or not total or not count:
                continue
            if '-' in (volume, total, count):
                continue
            try:
                yield RawItem(
                    id,
                    name.split(',')[0],
                    basis,
                    int(volume),
                    int(total),
                    int(count),
                    date
                    ).to_Item()
            except ValueError:
                yield RawItem(
                    id,
                    name.split(',')[0],
                    basis,
                    int(float(volume)*1000),
                    int(float(total)*1000),
                    int(float(count)*1000),
                    date
                    ).to_Item()
    except FileNotFoundError as e:
        logging.critical(e, exc_info=True)
