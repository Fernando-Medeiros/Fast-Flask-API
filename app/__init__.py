import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import routers
from setup import conf_database


def app() -> FastAPI:
    app = FastAPI(
        title="Fast-Flask-API",
        version="0.8.6",
        description="FFA is an api for a small social network",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(str(os.getenv("ALLOWED_HOSTS")).split(",")),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routers, prefix="/api")
    conf_database()
    return app
