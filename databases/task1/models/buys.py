import enum
from datetime import date

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from databases.task1.models import Base, pk


class StepVariants(enum.Enum):
    verified = 'проверка'
    collect = 'сборка'
    shipping = 'доставка'


class Step(Base):
    __tablename__ = 'steps'

    id: Mapped[pk]
    name: Mapped[StepVariants] = mapped_column(String)

    def __repr__(self):
        return f'{self.id}) {self.name}'


class BuyStep(Base):
    __tablename__ = 'buysteps'

    id: Mapped[pk]
    date_beg: Mapped[date] = mapped_column()
    date_end: Mapped[date] = mapped_column()
    step: Mapped[int] = mapped_column(ForeignKey('steps.id'))
    buy: Mapped[int] = mapped_column(ForeignKey('buys.id'))

    def __repr__(self):
        return f'{self.id}) {self.date_beg} - {self.date_end}'


class Buy(Base):
    __tablename__ = 'buys'

    id: Mapped[pk]
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    client: Mapped[int] = mapped_column(ForeignKey('clients.id'))

    def __repr__(self):
        return f'{self.id}) {self.description or "Default"}'


class BuyBook(Base):
    __tablename__ = 'buybooks'
    id: Mapped[pk]
    buy: Mapped[int] = mapped_column(ForeignKey('buys.id'))
    book: Mapped[int] = mapped_column(ForeignKey('books.id'))
    amount: Mapped[int] = mapped_column()

    def __repr__(self):
        return f'{self.id}) {self.amount} books'
