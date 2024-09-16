from typing import Annotated

from sqlalchemy.orm import DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    pass

pk = Annotated[int, mapped_column(primary_key=True)]