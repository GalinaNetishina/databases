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

    async def download(self) -> None:
        await self.producer()
        await self.process.join()

    def next_date(self):
        end = datetime.datetime.today().date()
        for i in range((end - self.start).days + 1):
            yield self.start + datetime.timedelta(days=i)

    async def produce(self, date) -> None:
        async with aiohttp.ClientSession() as session:
            file = await self._fetch_file(date, session)
            logging.debug(f"produce - {file}")
            if not file:
                return
            await self.process.put(asyncio.create_task(self.consume(file)))

    async def producer(self):
        await asyncio.gather(*(self.produce(i) for i in self.next_date()))

    async def consume(self, file) -> None:
        while True:
            try:
                logging.debug(f"{file} consume")
                await self.cb(extract_items(file))

                self.process.task_done()
                os.remove(file)
            except Exception as e:
                print(e)
                await asyncio.sleep(0.01)
                break

    @staticmethod
    async def _fetch_file(date: d, session) -> str:
        url = f'https://spimex.com//upload/reports/oil_xls/oil_xls_{date.strftime("%Y%m%d")}162000.xls'
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.read()
                filename = os.path.join("temp", f'{date.strftime("%Y%m%d")}.xls')
                await write_file(filename, data)
                return filename


def extract_items(file: str) -> Iterator[Item]:
    xls = xlrd.open_workbook_xls(file)
    sheet = xls.sheet_by_index(0)

    def is_not_ordered(*args: str) -> bool:
        return any(not i.isdigit() for i in args)

    def get_int(str_digit: str) -> int:
        try:
            return int(str_digit)
        except Exception:
            return int(float(str_digit) * 1000)

    for i in range(8, sheet.nrows - 2):
        _, id, name, basis, *tail = (sheet[i][j].value for j in range(sheet.ncols))
        volume, total, count = tail[0], tail[1], tail[5]
        date = datetime.datetime.strptime(file[-12:-4], "%Y%m%d").date()
        if is_not_ordered(volume, total, count):
            continue
        yield Item(
            exchange_product_id=id,
            exchange_product_name=name.split(",")[0],
            oil_id=id[:4],
            delivery_basis_id=id[4:7],
            delivery_basis_name=basis,
            delivery_type_id=id[-1],
            volume=get_int(volume),
            total=get_int(total),
            count=get_int(count),
            date=date,
        )
