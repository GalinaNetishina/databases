import logging
from collections import deque
from dataclasses import dataclass
from typing import Iterator, AsyncGenerator, Generator
import datetime as dt
from datetype import _date as d

import requests
from bs4 import BeautifulSoup as bs, ResultSet

from databases.task2.config import settings


@dataclass(frozen=True)
class Bulletin:
    date: d
    url: str

    def __repr__(self):
        return f'{self.date.strftime("%d-%m-%Y")}, url={self.url}'


class Scrapper:
    """
    create object with next properties:

    - default_date: date, before which the data is needed

    - bulletins: deque of Bulletins, with attributes date and url

    and method load_bulletins for receiving its from site
     """

    _base_url = 'https://spimex.com/'

    def __init__(self, date='15.09.2024'):
        self._default_date: dt.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self._bulletins = deque()

    @property
    def default_date(self) -> dt.date:
        return self._default_date

    @default_date.setter
    def default_date(self, date: dt.date) -> None:
        if type(date) == dt.date:
            self._default_date = date

    @property
    def bulletins(self) -> deque[Bulletin]:
        return self._bulletins

    @settings.time_check
    def load_bulletins(self):
        for res in self._scrap_next_page():
            if res.date <= self.default_date:
                logging.info(f"all data after {dt.datetime.strftime(res.date, '%d.%m.%Y')} received")
                break
            self._bulletins.append(res)
        return True

    def _scrap_next_page(self, page_count: int = 40):
        for page in range(1, page_count):
            url = f'https://spimex.com/markets/oil_products/trades/results/?page=page-{page}'
            response = requests.get(url)
            if response.status_code != 200:
                logging.error(f'response.status is not ok, {url=}')
                continue
            logging.debug(f'page#{page}')
            divs = bs(response.text, 'html.parser')
            divs = divs.findAll('div', class_='accordeon-inner__wrap-item')
            yield from self._extract_dates_and_urls(divs)

    def _extract_dates_and_urls(self, divs: ResultSet):
        for div, _ in zip(divs, range(10)):
            date = dt.datetime.strptime(div.find('span').text, '%d.%m.%Y').date()
            url = div.find('a', class_='accordeon-inner__item-title')['href']
            yield Bulletin(date, self.__class__._base_url + url)
