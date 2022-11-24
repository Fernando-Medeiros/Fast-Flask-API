from setup import conf_database

from fastapi import FastAPI

from .routes import router


def app() -> FastAPI:
    app = FastAPI()
    app.include_router(router, prefix='')
    conf_database()
    return app