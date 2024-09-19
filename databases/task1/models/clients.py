from typing import List

from pydantic import EmailStr
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.task1.models import BaseModel, pk


class City(BaseModel):
    __tablename__ = 'cities'
    __repr_attrs__ = ['name']

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String, unique=True)
    days_delivery: Mapped[int]


class Client(BaseModel):
    __tablename__ = 'clients'
    __repr_attrs__ = ['name', 'email']

    id: Mapped[pk]
    name: Mapped[str] = mapped_column()
    city: Mapped[int] = mapped_column(ForeignKey('cities.id'))
    email: Mapped[EmailStr] = mapped_column(String, unique=True)

    buys: Mapped[List['Buy']] = relationship(back_populates='client')
