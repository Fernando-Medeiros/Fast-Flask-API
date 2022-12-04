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
    client = TestClient(app())    
    utils = CaseAuth()
    
    client.post('/auth/', json=utils.data)
    login = client.post('/auth/login', data=utils.data, headers=utils.header)
    token = login.json()['access_token']
    
    client.headers['Authorization'] = f'bearer {token}'
    conf_database_test()
    return client