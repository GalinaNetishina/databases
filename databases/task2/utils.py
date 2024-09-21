import asyncio
import logging
import os
import requests
import xlrd
from collections import deque
from typing import NamedTuple, AsyncGenerator, Generator, Iterator
from datetype import _date as d


from databases.task2.models import Item
from databases.task2.orm import DB
from databases.task2.scrap import Bulletin


class Downloader:
    def __init__(self, source: deque[Bulletin], output_dir='temp'):
        self.input = source
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = os.path.join(output_dir)


    def _file(self, filename):
        return os.path.join(self.output_dir, f'{filename}.xls')

    async def loading(self):
        while True:
            portion = []
            for _ in range(10):
                if not self.input:
                    break
                portion.append(self.input.pop())
            tasks = [asyncio.create_task(self.transfer_data(i)) for i in portion]
            await asyncio.gather(*tasks)
            logging.info('portion is transfered')
            if not self.input:
                logging.info('deque is empty')
                break



    async def _download_file(self, item) -> d:
        response = requests.get(item.url, stream=True)
        path = self._file(item.date)
        if response.status_code == 200:
            with open(path, 'wb') as file:
                for chunk in response:
                    file.write(chunk)
            logging.debug(f'file {path} downloaded successfully')
            return item.date
        else:
            logging.error('Failed to download file')

    async def transfer_data(self, item) -> None:
        """from file.xls to Database"""
        filename = await self._download_file(item)
        path = self._file(filename)
        await DB.insert(self._extract_objects(filename))
        self.clean(path)

    @staticmethod
    def clean(path: str | bytes | os.PathLike[str] | os.PathLike[bytes]) -> None:
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def is_not_ordered(*args: str) -> bool:
        return any(not i.isdigit() for i in args)

    @staticmethod
    def get_int(str_digit: str) -> int:
        try:
            return int(str_digit)
        except:
            return int(float(str_digit) * 1000)

    def _extract_objects(self, filename: d) -> Iterator[Item]:
        """extracts Items from .xls file"""
        try:
            source = xlrd.open_workbook(self._file(filename))
            sheet = source.sheet_by_index(0)
            for i in range(8, sheet.nrows - 2):
                _, id, name, basis, *tail = (sheet[i][j].value for j in range(sheet.ncols))
                volume, total, count = tail[0], tail[1], tail[5]
                date = filename
                if self.is_not_ordered(volume, total, count):
                    continue
                yield Item(
                    exchange_product_id=id,
                    exchange_product_name=name,
                    oil_id=id[:4],
                    delivery_basis_id=id[4:7],
                    delivery_basis_name=basis,
                    delivery_type_id=id[-1],
                    volume=self.get_int(volume),
                    total=self.get_int(total),
                    count=self.get_int(count),
                    date=date
                )
        except FileNotFoundError as e:
            logging.error(e, exc_info=True)
