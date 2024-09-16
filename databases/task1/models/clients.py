import enum

from pydantic import EmailStr
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from databases.task1.models import Base, pk


class StepVariants(enum.Enum):
    verified = 'проверка'
    collect = 'сборка'
    shipping = 'доставка'


class City(Base):
    __tablename__ = 'cities'

    id: Mapped[pk]
    name: Mapped[str] = Column(String, unique=True)
    days_delivery: Mapped[int] = mapped_column()

    def __repr__(self):
        return f'{self.name} (delivery takes{self.days_delivery} days)'


class Client(Base):
    __tablename__ = 'clients'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column()
    city: Mapped[int | None] = mapped_column(ForeignKey('cities.id'))
    email: Mapped[EmailStr] = mapped_column(String, unique=True)

    def __repr__(self):
        return f'{self.id}){self.name}'


class Step(Base):
    __tablename__ = 'steps'

    id: Mapped[pk]
    name: Mapped[StepVariants] = mapped_column(String)

    def __repr__(self):
        return f'{self.id}) {self.name}'


