from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass


class Genre(BaseModel):
    id: int
    name: str


class Author(BaseModel):
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
    date_end: date = Field()
    step: int
    buy: int

    @field_validator("date_end")
    def fi(cls, v, fields) -> date:
        if v < fields['data_beg']:
            raise ValueError('date of end must be after date of beginning')
        return v


class Buy(BaseModel):
    id: int
    description: str
    client: int


class BuyBook(BaseModel):
    id: int
    buy: int
    client: int
    amount: int = Field(gt=0)
