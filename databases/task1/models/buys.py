import enum
from datetime import date

from sqlalchemy import ForeignKey, String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from databases.task1.models import BaseModel, pk


class StepVariants(str, enum.Enum):
    VERIFICATION = 'проверка'
    COLLECTION = 'сборка'
    SHIPPING = 'доставка'


class Step(BaseModel):
    __tablename__ = 'steps'
    __repr_attrs__ = ['name']

    id: Mapped[pk]
    name: Mapped[StepVariants] = mapped_column(String)


class BuyStep(BaseModel):
    __tablename__ = 'buysteps'
    __repr_attrs__ = ['step', 'date_beg', 'date_end']

    id: Mapped[pk]
    date_beg: Mapped[date] = mapped_column()
    date_end: Mapped[date] = mapped_column()
    step_id: Mapped[int] = mapped_column(ForeignKey('steps.id'))
    buy_id: Mapped[int] = mapped_column(ForeignKey('buys.id', ondelete='CASCADE'))


class Buy(BaseModel):
    __tablename__ = 'buys'
    __repr_attrs__ = ['description']

    id: Mapped[pk]
    description: Mapped[str] = mapped_column(String(256), nullable=True)
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.id', ondelete='CASCADE'))
    client: Mapped['Client'] = relationship(back_populates='buys')
    book: Mapped['Book'] = relationship(back_populates='buy', secondary='buybooks')


class BuyBook(BaseModel):
    __tablename__ = 'buybooks'
    __repr_attrs__ = ['book', 'client', 'amount']

    id: Mapped[pk]
    buy_id: Mapped[int] = mapped_column(ForeignKey('buys.id', ondelete='CASCADE'))
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    amount: Mapped[int] = mapped_column()

    __table_args__ = (
        CheckConstraint('amount > 0', 'check amount positive'),
    )

