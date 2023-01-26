import os

import databases
import sqlalchemy
from dotenv import find_dotenv, load_dotenv
from ormar import ModelMeta

load_dotenv(find_dotenv())


def get_database_uri() -> str:
    ENV = os.getenv("ENV", None)

    match ENV:
        case "DEV":
            return os.getenv("DATABASE_DEV_URL", "sqlite:///dbDev.sqlite")
        case "TEST":
            return os.getenv("DATABASE_TEST_URL", "sqlite:///dbTest.sqlite")
        case "PRO":
            try:
                user = os.environ["DATABASE_USERNAME"]
                password = os.environ["DATABASE_PASSWORD"]
                host = os.environ["DATABASE_HOST"]
                port: int = int(os.environ["DATABASE_PORT"])
                db_name = os.environ["DATABASE_NAME"]

            except (ValueError, IndexError) as args:
                raise ValueError(args)
            else:
                return "postgresql://{}:{}@{}:{}/{}".format(
                    user, password, host, port, db_name
                )


DB_URI = get_database_uri()
database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()


class BaseMeta(ModelMeta):
    metadata = metadata
    database = database


def conf_database():
    engine = sqlalchemy.create_engine(DB_URI)
    metadata.create_all(engine)


def conf_database_test():
    engine = sqlalchemy.create_engine(DB_URI)
    metadata.drop_all(engine)
    metadata.create_all(engine)


async def startup():
    await database.connect()


async def shutdown():
    await database.disconnect()
