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
from scrap import Bulletin, Scrapper


async def write_file(filename, data):
    async with aiofiles.open(filename, "wb") as file:
        await file.write(data)


async def _fetch_file(item: Bulletin, session) -> None:
    async with session.get(item.url) as response:
        data = await response.read()
        filename = os.path.join("temp", f"{item.date}.xls")
        await write_file(filename, data)


class Downloader:
    def __init__(self, source: deque[Bulletin], output_dir: str = "temp"):
        self.input = source
        os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir
        self.output = deque()

    def _file(self, filename: d) -> str | os.PathLike[str]:
        return os.path.join(self.output_dir, f"{filename}.xls")

    async def next_portion(self) -> bool:
        """append Items, extracted from few files, to self.output deque"""
        if not self.input:
            logging.info("source deque is empty")
            return False
        portion = []
        for _ in range(10):
            if not self.input:
                break
            portion.append(self.input.pop())
        tasks = [asyncio.create_task(self.extract_to_output(i)) for i in portion]
        await asyncio.gather(*tasks)
        # logging.info('portion is extracted')
        return True

    async def extract_to_output(self, item) -> None:
        """from file.xls to self.output deque"""
        e = Extractor(self._file(item.date))
        with e:
            self.output.append(e.objects)

    async def download(self) -> None:
        async with aiohttp.ClientSession() as session:
            tasks = [
                asyncio.create_task(_fetch_file(item, session)) for item in self.input
            ]
            await asyncio.gather(*tasks)


class Extractor:
    def __init__(self, file: str | os.PathLike[str]):
        self.source = file

    def __enter__(self):
        self.xls = xlrd.open_workbook(self.source)
        self.sheet = self.xls.sheet_by_index(0)

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
            date = datetime.datetime.strptime(self.source[-14:-4], "%Y-%m-%d").date()
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
