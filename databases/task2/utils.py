import asyncio
import datetime
import logging
import os
from collections import deque

import aiohttp
import xlrd
from typing import Iterator, Callable
from datetype import _date as d
import aiofiles

from models import Item


async def write_file(filename, data):
    async with aiofiles.open(filename, "wb") as file:
        await file.write(data)


class Downloader:
    def __init__(self, start: str, send_to: Callable):
        self.start: datetime.date = datetime.datetime.strptime(start, "%d.%m.%Y").date()
        self.cb = send_to
        self.output_dir = "temp"
        os.makedirs("temp", exist_ok=True)
        self.process = asyncio.Queue()
        self.output = deque()

    async def download_1(self) -> None:
        await asyncio.gather(self.produce())
        await asyncio.gather(self.consume())

    async def download_2(self) -> None:
        await asyncio.gather(self.produce(), self.consume())

    async def resend(self):
        while self.output:
            data = self.output.pop()
            await self.cb(data)

    async def produce(self) -> None:
        async with aiohttp.ClientSession() as session:
            end = datetime.datetime.today().date()
            for i in range((end - self.start).days + 1):
                file = await self._fetch_file(
                    self.start + datetime.timedelta(days=i), session
                )
                if not file:
                    continue
                await self.process.put(file)
            await self.process.put(None)

    async def consume(self) -> None:
        """from self.process que with filenames to self.output que"""
        while True:
            item = await self.process.get()
            if item is None:
                break
            # logging.info(f"consume item...{item}")
            self.extract_to_output(item)
            await self.resend()

    @staticmethod
    async def _fetch_file(date: d, session) -> str:
        url = f'https://spimex.com//upload/reports/oil_xls/oil_xls_{date.strftime("%Y%m%d")}162000.xls'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                filename = os.path.join("temp", f'{date.strftime("%Y%m%d")}.xls')
                await write_file(filename, data)
                return filename

    def extract_to_output(self, filename) -> None:
        """from file.xls to self.output deque"""
        e = Extractor(filename)
        with e:
            self.output.append(e.objects)


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
