import os

import databases
import sqlalchemy
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


def get_database_uri() -> str:

    ENVIRONMENT = os.getenv("ENVIRONMENT", None)

    if ENVIRONMENT == "DEVELOPMENT":
        return os.getenv("DATABASE_TEST_URL", "sqlite:///db.sqlite")

    try:
        user = os.environ["DATABASE_USERNAME"]
        password = os.environ["DATABASE_PASSWORD"]
        host = os.environ["DATABASE_HOST"]
        port = int(os.environ["DATABASE_PORT"])
        db_name = os.environ["DATABASE_NAME"]

    except (ValueError, IndexError, IndexError) as args:
        raise ValueError(args)
    else:
        uri = "postgresql://{}:{}@{}:{}/{}".format(user, password, host, port, db_name)
        return uri


DB_URI = get_database_uri()
database = databases.Database(DB_URI)
metadata = sqlalchemy.MetaData()


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
