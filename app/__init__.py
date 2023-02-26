import os

import cloudinary
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import routers
from .services.storage import get_cloud_storage_credentials
from .services.database import AsyncDatabase, BuildDatabase


def app() -> FastAPI:
    app = FastAPI(
        title="Fast-Flask-API",
        version="1.2.1",
        description="FFA is an api for a small social network",
        on_startup=[AsyncDatabase.startup],
        on_shutdown=[AsyncDatabase.shutdown],
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=str(os.getenv("ALLOWED_HOSTS")).split(","),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    cloudinary.config(**get_cloud_storage_credentials())

    app.include_router(routers, prefix="/api/v1")

    BuildDatabase.build_database()

    return app
