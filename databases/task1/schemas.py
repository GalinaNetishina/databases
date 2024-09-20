from datetime import date

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from pydantic.dataclasses import dataclass

from databases.task1.models import *


class GenrePOST(BaseModel):
    name: str


class GenreGET(GenrePOST):
    id: int


class AuthorPOST(BaseModel):
    name: str


class AuthorGET(AuthorPOST):
    id: int


class BookPOST(BaseModel):
    title: str
    author: Author
    genre: Genre


class BookGET(BookPOST):
    id: int


class CityPOST(BaseModel):
    name: str
    days_delivery: int


class CityGET(CityPOST):
    id: int


class ClientPOST(BaseModel):
    name: str
    city: int
    email: EmailStr


class ClientGET(ClientPOST):
    id: int

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
