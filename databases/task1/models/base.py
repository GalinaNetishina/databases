from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column, scoped_session, sessionmaker


from .mixins import ReprMixin


class Base(DeclarativeBase):
    pass


class BaseModel(ReprMixin, Base):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__


pk = Annotated[int, mapped_column(primary_key=True)]
