from typing import List

from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel, pk


class Genre(BaseModel):
    __tablename__ = 'genres'
    __repr_attrs__ = ['name']

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    books: Mapped[List['Book']] = relationship(back_populates='genre')


class Author(BaseModel):
    __tablename__ = 'authors'
    __repr_attrs__ = ['name']

    id: Mapped[pk]
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    books: Mapped[List['Book']] = relationship(back_populates='author')

    __table_args__ = (
        Index('author_name_index', 'name'),
    )


class Book(BaseModel):
    __tablename__ = 'books'
    __repr_attrs__ = ['title', 'author', 'genre']

    id: Mapped[pk]
    title: Mapped[str] = mapped_column(String, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    genre_id: Mapped[int] = mapped_column(ForeignKey('genres.id'))

    author: Mapped['Author'] = relationship(back_populates='books')
    genre: Mapped[List['Genre']] = relationship(back_populates='books')
    buy: Mapped['Buy'] = relationship(back_populates='book', secondary='buybooks')

    __table_args__ = (
        Index('title_index', 'title'),
    )