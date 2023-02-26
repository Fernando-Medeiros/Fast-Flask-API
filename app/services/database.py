import os

import databases
import sqlalchemy
from dotenv import find_dotenv, load_dotenv
from ormar import ModelMeta

load_dotenv(find_dotenv())


def get_database_uri() -> str:
    ENV: str = os.getenv("ENV", "DEV")
    URI: str = ""

    match ENV:
        case "DEV":
            URI = os.getenv("DATABASE_DEV_URL", "sqlite:///dbDev.sqlite")
        case "TEST":
            URI = os.getenv("DATABASE_TEST_URL", "sqlite:///dbTest.sqlite")
        case "PRO":
            try:
                username = os.environ["DATABASE_USERNAME"]
                password = os.environ["DATABASE_PASSWORD"]
                host = os.environ["DATABASE_HOST"]
                port: int = int(os.environ["DATABASE_PORT"])
                database = os.environ["DATABASE_NAME"]

            except (ValueError, IndexError) as args:
                raise ValueError(args)
            else:
                URI = "postgresql://{}:{}@{}:{}/{}".format(
                    username, password, host, port, database
                )
    return URI


DB_URI: str = get_database_uri()
database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


class BuildDatabase:
    @staticmethod
    def build_database():
        engine = sqlalchemy.create_engine(DB_URI)
        metadata.create_all(engine)

    @staticmethod
    def build_database_test():
        engine = sqlalchemy.create_engine(DB_URI)
        metadata.drop_all(engine)
        metadata.create_all(engine)


class AsyncDatabase:
    @staticmethod
    async def startup():
        await database.connect()

    @staticmethod
    async def shutdown():
        await database.disconnect()
