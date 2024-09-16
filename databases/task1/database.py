from sqlalchemy import create_engine
from sqlalchemy.orm import create_session

from config import settings



#DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
#DATABASE_URL = 'sqlite:///book_delivery.db'


sync_engine = create_engine(settings.DSN_postgresql_psycopg)
def session_factory():
    return create_session(bind=sync_engine)





