#from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy import select

from databases.task2.database import sync_engine, session_factory
from databases.task2.models import *


class SyncORM:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)

    @staticmethod
    def insert(*args):
        with session_factory() as session:
            session.add_all(args)
            session.commit()

    @staticmethod
    def show():
        with session_factory() as session:
            query = select(Item)
            res = session.execute(query).all()
            print(*(i[0] for i in res), sep='\n')








# metadata = MetaData()
# spimex_trading_result = Table(
#     'spimex_trading_result', metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('exchange_product_id', String(12)),
#     Column('exchange_product_name', String(80)),
#     Column('delivery_basis_name', String(30)),
#     Column('oil_id', String),
#     Column('delivery_basis_id', String),
#     Column('delivery_type_id', String),
#     Column('volume', Integer),
#     Column('total', Integer),
#     Column('count', Integer),
#     Column(' date', String(20)),
#     Column('created_on', String(20)),
#     Column('updated_on', String(20), nullable=True)
# )


