import asyncio
import os
import sys

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from databases.task1.orm import DB

sys.path.insert(1, os.path.join(sys.path[0], 'databases'))

def create_fastapi_app():
    app = FastAPI(title="FastAPI")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
    )

    @app.get("/books", tags=["Books"])
    async def get_workers():
        books = DB.convert_Books_to_dto()
        return books

    @app.get("/authors", tags=["Резюме"])
    async def get_resumes():
        resumes = DB.select_authors()
        return resumes

    @app.get('/')
    def get_home():
        return "<h1>Hello, World!</h1>"

    return app


app = create_fastapi_app()

if __name__ == "__main__":

    if "--webserver" in sys.argv:
        uvicorn.run(
            app="src.main:app",
            reload=True,
        )
