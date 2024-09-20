from sqlalchemy import create_engine
from sqlalchemy.orm import create_session, sessionmaker

from config import settings

sync_engine = create_engine(settings.DSN_postgresql_psycopg, echo=True)
session_factory = sessionmaker(sync_engine)
