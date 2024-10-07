import asyncio
import datetime
import logging
import os

import aiohttp
import xlrd
from collections import deque
from typing import Iterator
from datetype import _date as d
import aiofiles

from models import Item


async def write_file(filename, data):
    async with aiofiles.open(filename, "wb") as file:
        await file.write(data)


class Downloader:
    def __init__(self, start: str = "01.10.2024"):
        start: datetime.date = datetime.datetime.strptime(start, "%d.%m.%Y").date()
        end = datetime.datetime.today().date()
        self.period = [
            start + datetime.timedelta(days=i) for i in range((end - start).days + 1)
        ]
        self.output_dir = "temp"
        os.makedirs("temp", exist_ok=True)
        self.output = deque()

    @staticmethod
    async def _fetch_file(date: d, session) -> None:
        url = f'https://spimex.com//upload/reports/oil_xls/oil_xls_{date.strftime("%Y%m%d")}162000.xls'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                filename = os.path.join("temp", f'{date.strftime("%Y%m%d")}.xls')
                await write_file(filename, data)

    async def extract_to_output(self, filename) -> None:
        """from file.xls to self.output deque"""
        e = Extractor(filename)
        with e:
            self.output.append(e.objects)

    async def download(self) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [
                    asyncio.create_task(self._fetch_file(date, session))
                    for date in self.period
                ]
                await asyncio.gather(*tasks)
            logging.info(f"all data after {self.period[0]} received")
            tasks = []
            for date in self.period:
                filename = os.path.join("temp", f'{date.strftime("%Y%m%d")}.xls')
                tasks.append(self.extract_to_output(filename))
            await asyncio.gather(*tasks)
        except FileNotFoundError:
            pass


class Extractor:
    def __init__(self, file: str | os.PathLike[str]):
        self.source = file

    def __enter__(self):
        try:
            self.xls = xlrd.open_workbook_xls(self.source)
            self.sheet = self.xls.sheet_by_index(0)
        except FileNotFoundError:
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.remove(self.source)

    @staticmethod
    def is_not_ordered(*args: str) -> bool:
        return any(not i.isdigit() for i in args)

    @staticmethod
    def get_int(str_digit: str) -> int:
        try:
            return int(str_digit)
        except:
            return int(float(str_digit) * 1000)

    @property
    def objects(self) -> Iterator[Item]:
        """returns iterator of Items, extracted from .xls file"""
        for i in range(8, self.sheet.nrows - 2):
            _, id, name, basis, *tail = (
                self.sheet[i][j].value for j in range(self.sheet.ncols)
            )
            volume, total, count = tail[0], tail[1], tail[5]
            date = datetime.datetime.strptime(self.source[-12:-4], "%Y%m%d").date()
            if self.is_not_ordered(volume, total, count):
                continue
            yield Item(
                exchange_product_id=id,
                exchange_product_name=name.split(",")[0],
                oil_id=id[:4],
                delivery_basis_id=id[4:7],
                delivery_basis_name=basis,
                delivery_type_id=id[-1],
                volume=self.get_int(volume),
                total=self.get_int(total),
                count=self.get_int(count),
                date=date,
            )
