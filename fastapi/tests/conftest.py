import pytest
from app import app
from setup import conf_database_test

from fastapi.testclient import TestClient


@pytest.fixture(scope='function')
def client():
    conf_database_test()
    with TestClient(app()) as client:
        yield client