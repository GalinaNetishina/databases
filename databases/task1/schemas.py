from datetime import date

from pydantic import BaseModel, EmailStr
from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class Genre:
    id: int
    name: str


@dataclass(frozen=True)
class Author:
    id: int
    name: str


class Book(BaseModel):
    id: int
    title: str
    author: int
    genre: int


class City(BaseModel):
    id: int
    name: str
    days_delivery: int


class Client(BaseModel):
    id: int
    name: str
    city: int
    email: EmailStr


class Step(BaseModel):
    id: int
    name: str


class BuyStep(BaseModel):
    id: int
    date_beg: date
    date_end: date
    step: int
    buy: int


class Buy(BaseModel):
    id: int
    description: str
    client: int


class BuyBook(BaseModel):
    id: int
    buy: int
    client: int
    amount: int
