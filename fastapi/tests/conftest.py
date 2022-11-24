import pytest
from app import app
from setup import conf_database

from fastapi.testclient import TestClient


@pytest.fixture(scope='function')
def client():
    conf_database(test=True)
    with TestClient(app()) as client:
        yield client