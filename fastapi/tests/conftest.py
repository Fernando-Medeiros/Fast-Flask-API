import pytest
from app import app
from setup import conf_database_test

from fastapi.testclient import TestClient

from .utils.user import CaseLogin


@pytest.fixture(scope='function')
def client():
    conf_database_test()
    with TestClient(app()) as client:
        yield client


@pytest.fixture(scope='function')
def client_one():
    conf_database_test()
    client = TestClient(app())
    client.post('/user/', json=CaseLogin().valid_user)
    return client


@pytest.fixture(scope='function')
def client_two_header_auth():
    conf_database_test()
    client = TestClient(app()) 
    client.post('/user/', json=CaseLogin().valid_user)
    login = client.post(
        '/auth/token', data=CaseLogin().login, headers=CaseLogin().content_type)
    
    token = login.json()['access_token']
    client.headers['Authorization'] = f'bearer {token}'
    return client