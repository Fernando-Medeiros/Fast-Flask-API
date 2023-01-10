import os

import databases
import sqlalchemy
from dotenv import find_dotenv, load_dotenv

# lOAD .ENV
load_dotenv(find_dotenv())

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')

database = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()


def conf_database():
    engine = sqlalchemy.create_engine(DB_URL)
    metadata.create_all(engine)


def conf_database_test():
    engine = sqlalchemy.create_engine(DB_URL)
    metadata.drop_all(engine)
    metadata.create_all(engine)