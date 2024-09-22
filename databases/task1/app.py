from typing import Annotated

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from models import *
from schemas import AuthorPOST
from orm import DB

templates = Jinja2Templates(directory="templates")


def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/books", tags=["Books"])
    async def get_books():
        return DB.books_dto()

    @app.get("/authors", tags=["Authors"])
    async def get_authors():
        return DB.authors_dto()

    @app.post("/author")
    async def post_author(
            author: Annotated[AuthorPOST, Depends()]
    ):

        DB.add_data([Author(**author.dict())])
        return {'status': 201}

    @app.get("/genres", tags=["Genres"])
    async def get_genres():
        return DB.genres_dto()

    @app.get('/index/{target}', response_class=HTMLResponse)
    def index(target: str, request: Request):
        return templates.TemplateResponse("index.html", {"request": request, "target": target})

    return app


app = create_fastapi_app()
