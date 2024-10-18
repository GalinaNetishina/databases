from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, status, BackgroundTasks
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis

from router import router as root
from config import settings

logging.basicConfig(level=logging.DEBUG, format=" %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True,
    )
    # await loading()
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Spimex Trading Results", lifespan=lifespan)
app.include_router(root)

origins = [f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}",
           f"http://{settings.REDIS_HOST}:{settings.REDIS_PORT}"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# async def loading():
#     from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
#     from datetime import datetime, timedelta
#     from functools import partial
#     from database import async_engine
#     from repository import Repository
#     from var2 import Downloader
#     session_maker = async_sessionmaker(
#         bind=async_engine,
#         class_=AsyncSession,
#         autoflush=False,
#         autocommit=False,
#         expire_on_commit=False,
#     )
#     async with session_maker() as session:
#         after = "01.10.2024"
#         try:
#             dates = await Repository.get_last_trading_dates(session, 1)
#             if datetime.today().date() - dates[0].date > timedelta(days=3):
#                 after = dates[0].date.strftime("%d.%m.%Y")
#                 dl = Downloader(after, partial(Repository.add_many, session))
#                 await dl.download()
#                 logging.debug('data loading')
#             else:
#                 logging.debug('data still fresh')
#                 return
#         except Exception as e:
#             print(e)
#         finally:
#             await session.commit()
