from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware

from redis import asyncio as aioredis
from pydantic import ValidationError
from fastapi.responses import JSONResponse

from router import router as root
from tasks.router import router as back
from config import settings


# logging.basicConfig(level=logging.DEBUG, format=" %(message)s")


# async def test_load() -> None:
#     after = await Repo.get_last_trading_dates(1)
#     if datetime.today().date() - after[0].date > timedelta(days=3):
#         after = after[0].date.strftime("%d.%m.%Y")
#         dl = Downloader(after, Repo.add_many)
#         await dl.download()
#         print("load to DB complete")


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    # await test_load()
    yield


app = FastAPI(title="Spimex Trading Results", lifespan=lifespan)
app.include_router(root)
app.include_router(back)

origins = [f"http://{settings.FRONTEND_HOST}:{settings.FRONTEND_PORT}"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )


# @app.on_event('startup')
# async def startup_event():
#     redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
