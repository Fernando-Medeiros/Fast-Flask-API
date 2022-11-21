from fastapi import FastAPI

from .routes import router


def app():
    app = FastAPI()
    app.include_router(router, prefix='')
    return app