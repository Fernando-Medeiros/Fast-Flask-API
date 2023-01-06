import pytest
from app import app
from setup import conf_database_test

from fastapi.testclient import TestClient

from .utils.user import CaseAuth


@pytest.fixture(scope='function')
def client():
    conf_database_test()
    with TestClient(app()) as client:
        yield client


@pytest.fixture(scope='function')
def client_auth():
    conf_database_test()
    client = TestClient(app())    
    utils = CaseAuth()
    
    client.post('/user/', json=utils.valid_user)
    login = client.post('/auth/token', data=utils.data, headers=utils.header)
    token = login.json()['access_token']
    
    client.headers['Authorization'] = f'bearer {token}'

    return client