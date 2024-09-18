import logging
from dataclasses import dataclass
from typing import Iterator, AsyncGenerator
import datetime as dt
from datetype import _date as d

import requests
from bs4 import BeautifulSoup as bs


@dataclass(frozen=True)
class Bulletin:
    date: d
    url: str

    async def download_file(self, filename) -> None:
        base_url = 'https://spimex.com/'
        url = base_url + self.url
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'temp/{filename}', 'wb') as file:
                file.write(response.content)
            logging.debug('file downloaded successfully')
        else:
            logging.error('Failed to download file')

    def __repr__(self):
        return f'{self.date.strftime("%d-%m-%Y")}, url={self.url}'


class Scrapper:
    """
    create object with next properties:

    - default_date: date, before which the data is needed

    - bulletins: generates sequence of Bulletins, with attributes date and relative url
     """
    def __init__(self, date='10.09.2024'):
        self._default_date: dt.date = dt.datetime.strptime(date, '%d.%m.%Y').date()

    @property
    def default_date(self) -> dt.date:
        return self._default_date

    @default_date.setter
    def default_date(self, date: dt.date) -> None:
        if type(date) == dt.date:
            self._default_date = date

    def _get_page(self, limit: int | None = None) -> Iterator[bs]:
        page = 0
        while True:
            page += 1
            url = f'https://spimex.com/markets/oil_products/trades/results/?page=page-{page}'
            response = requests.get(url)
            if limit and page > limit:
                logging.info(f'limit reached')
                return
            if response.status_code != 200:
                logging.error(f'response.status is not ok, {url=}')
                return
            logging.debug(f'page#{page}')
            yield bs(response.text, 'html.parser')

    @property
    async def bulletins(self) -> AsyncGenerator[Bulletin, None]:
        pages = self._get_page()
        for _, page in enumerate(pages):
            divs = page.findAll('div', class_='accordeon-inner__wrap-item')
            for div, _ in zip(divs, range(10)):
                date = dt.datetime.strptime(div.find('span').text, '%d.%m.%Y').date()
                url = div.find('a', class_='accordeon-inner__item-title')['href']
                if date <= self.default_date:
                    logging.info(f'all data before {dt.datetime.strftime(date, "%d.%m.%Y")} received')
                    return
                yield Bulletin(date, url)


scrapper = Scrapper()
