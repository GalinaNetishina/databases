import random

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from faker import Faker

from database import session_factory, sync_engine as se
from models import *
from schemas import *

faker = Faker()


class DB:
    @staticmethod
    def create_tables():
        engine = se
        engine.echo = False
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.echo = True

    @staticmethod
    def add_data(data: list[BaseModel]):
        with session_factory() as ses:
            ses.add_all(data)
            ses.commit()

    @staticmethod
    def all_books():
        with session_factory() as ses:
            query = (
                select(Book)
                .options(joinedload(Book.author))
                .options(selectinload(Book.genre))
                .order_by(Book.title)
            )
            res = ses.execute(query)
            return res.scalars().all()

    @staticmethod
    def all_authors():
        with session_factory() as ses:
            query = (
                select(Author)
                .order_by(Author.name)
            )
            res = ses.execute(query)
            return res.scalars().all()

    @staticmethod
    def all_genres():
        with session_factory() as ses:
            query = (
                select(Genre)
                .order_by(Genre.name)
            )
            res = ses.execute(query)
            return res.scalars().all()

    @staticmethod
    def books_dto():
        result_dto = [BookGET.model_validate(row, from_attributes=True) for row in DB.all_books()]
        return result_dto

    @staticmethod
    def authors_dto():
        result_dto = [AuthorGET.model_validate(row, from_attributes=True) for row in DB.all_authors()]
        return result_dto

    @staticmethod
    def genres_dto():
        result_dto = [GenreGET.model_validate(row, from_attributes=True) for row in DB.all_genres()]
        return result_dto

    @staticmethod
    def fill_with_fake():
        with session_factory() as ses:
            authors = ses.query(Author).all() or [Author(name=faker.name()) for _ in range(20)]
            genres = ses.query(Genre).all() or [Genre(name=faker.word()) for _ in range(10)]
            books = [
                Book(
                    title=faker.name(),
                    author=random.choice(authors),
                    genre=random.choice(genres))
                for _ in range(1)
            ]
            ses.add_all(books)
            ses.commit()
