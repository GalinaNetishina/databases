from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from config import settings

sync_engine = create_engine(settings.DSN_postgresql_psycopg)


def session_factory():
    return create_session(bind=sync_engine)
