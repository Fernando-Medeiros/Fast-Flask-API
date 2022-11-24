import os

import databases
import sqlalchemy
from dotenv import find_dotenv, load_dotenv

# lOAD .ENV
load_dotenv(find_dotenv())

DB_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite')

database = databases.Database(DB_URL)
metadata = sqlalchemy.MetaData()

def conf_database(test: bool = False):
    engine = sqlalchemy.create_engine(DB_URL)

    if test:
        metadata.drop_all(engine)

    metadata.create_all(engine)
