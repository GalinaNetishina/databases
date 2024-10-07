import logging
from collections import deque
from typing import Iterator, NamedTuple
import datetime
from datetype import _date as d

import requests
from bs4 import BeautifulSoup as bs, ResultSet

from config import settings


class Bulletin(NamedTuple):
    date: d
    url: str


class Scrapper:
    """
    create object with next properties:

    - default_date: date, before which the data is needed

    - bulletins: deque of Bulletins, with attributes date and url

    and method load_bulletins for receiving its from site
    """

    _base_url = "https://spimex.com/"

    def __init__(self, date: str = "01.01.2023"):
        self._default_date: datetime.date = datetime.datetime.strptime(
            date, "%d.%m.%Y"
        ).date()
        self._bulletins = deque()

    @property
    def default_date(self) -> d:
        return self._default_date

    @default_date.setter
    def default_date(self, date: d) -> None:
        if type(date) == datetime.date:
            self._default_date = date

    @property
    def bulletins(self) -> deque[Bulletin]:
        return self._bulletins

    @settings.time_check
    def load_bulletins(self) -> None:
        for res in self._scrap_next_page():
            if res.date <= self.default_date:
                logging.info(f"all data after {res.date} received")
                break
            self._bulletins.append(res)

    def _scrap_next_page(self, page_count: int = 40) -> Iterator[Bulletin]:
        for page in range(1, page_count):
            url = f"https://spimex.com/markets/oil_products/trades/results/?page=page-{page}"
            response = requests.get(url)
            if response.status_code != 200:
                logging.error(f"response.status is not ok, {url=}")
                continue
            logging.debug(f"page#{page}")
            divs = bs(response.text, "html.parser").findAll(
                "div", class_="accordeon-inner__wrap-item"
            )
            yield from self._get_bulletins(divs)

    def _get_bulletins(self, divs: ResultSet) -> Iterator[Bulletin]:
        for div, _ in zip(divs, range(10)):
            date = datetime.datetime.strptime(div.find("span").text, "%d.%m.%Y").date()
            url = div.find("a", class_="accordeon-inner__item-title")["href"]
            yield Bulletin(date, self.__class__._base_url + url)
