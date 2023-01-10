import os

from setup import conf_database

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router


def app() -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(str(os.getenv('ALLOWED_HOSTS')).split(',')),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        )
    
    app.include_router(router, prefix='')
    conf_database()
    return app