from pydantic import BaseModel as BM, EmailStr as ES, Field, field_validator


from models import *


class GenrePOST(BM):
    name: str


class GenreGET(GenrePOST):
    id: int


class AuthorPOST(BM):
    name: str


class AuthorGET(AuthorPOST):
    id: int


class BookPOST(BM):
    title: str
    author: "AuthorGET"
    genre: "GenreGET"


class BookGET(BookPOST):
    id: int


class CityPOST(BM):
    name: str
    days_delivery: int


class CityGET(CityPOST):
    id: int


class ClientPOST(BM):
    name: str
    city: int
    email: str


class ClientGET(ClientPOST):
    id: int


class Step(BM):
    id: int
    name: str


class BuyStep(BM):
    id: int
    date_beg: date
    date_end: date = Field()
    step: int
    buy: int

    @field_validator("date_end")
    def fi(cls, v, fields) -> date:
        if v < fields["data_beg"]:
            raise ValueError("date of end must be after date of beginning")
        return v


class Buy(BM):
    id: int
    description: str
    client: int


class BuyBook(BM):
    id: int
    buy: int
    client: int
    amount: int = Field(gt=0)
