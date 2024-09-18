from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from databases.task1.models.base import Base, pk


class Genre(Base):
    __tablename__ = 'genres'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(nullable=False, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.id}) {self.name}'


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    genre: Mapped[str] = mapped_column(ForeignKey('genres.id'))

    def __repr__(self):
        return f'{self.id}) {self.title}'
