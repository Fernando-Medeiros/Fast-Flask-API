import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import routers
from setup import conf_database, shutdown, startup


def app() -> FastAPI:
    app = FastAPI(
        title="Fast-Flask-API",
        version="1.1.2",
        description="FFA is an api for a small social network",
        on_startup=[startup],
        on_shutdown=[shutdown],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(str(os.getenv("ALLOWED_HOSTS")).split(",")),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routers, prefix="/api/v1")
    conf_database()
    return app
