import random

from sqlalchemy import select, func
from sqlalchemy.orm import joinedload, selectinload
from faker import Faker

from databases.task1.database import session_factory, sync_engine as se
from databases.task1.models import *

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
    def get_data() :
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
