from databases.task1.database import session_factory, sync_engine as se
from databases.task1.models import *


class DB:
    @staticmethod
    def create_tables():
        engine = se
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

    @staticmethod
    def add_data(data: list[BaseModel]):
        with session_factory() as ses:
            ses.add_all(data)
            ses.commit()

    @staticmethod
    def get_data(target: Base):
        with session_factory() as ses:
            return ses.query(target)



