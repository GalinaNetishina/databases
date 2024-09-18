from typing import Annotated
import datetime as dt

from sqlalchemy import text, BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


created_at = Annotated[dt.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"))]

updated_at = Annotated[dt.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    server_onupdate=text("TIMEZONE('utc', now())")
)]


class Item(Base):
    __tablename__ = 'spimex_trading_results'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    delivery_basis_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int] = mapped_column(BigInteger)
    count: Mapped[int]
    date: Mapped[dt.date]
    created_on: Mapped[created_at]
    updated_on: Mapped[updated_at]

    def __repr__(self):
        return f'{self.date} : {self.exchange_product_name:80}| {self.count:6} договоров| {self.created_on.date()}'

