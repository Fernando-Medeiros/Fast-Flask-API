import pytest
from app.utils.token_jwt import DecodeTokenJwt

from fastapi.testclient import TestClient

from ..utils.user import CaseLogin

utils = CaseLogin()

# LOGIN - TOKEN
@pytest.mark.token
def test_login_valid_user(client: TestClient):    
    user_attr, login_attr = utils.valid_user, utils.valid_login
    headers = ['access_token', 'token_type']
    
    client.post('/user/', json=user_attr)
    
    response = client.post('/auth/token', data=login_attr)
    context = response.json()    
    
    token = DecodeTokenJwt().decode(context['access_token'])

    assert response.status_code == 200
    assert [context[key] for key in headers]
    assert token['id']


# AUTHENTICATED CLIENT WITH BEARER
@pytest.mark.userAuth
def test_authenticated_client(client_auth: TestClient):
    assert DecodeTokenJwt().decode(
        client_auth.headers['Authorization'].replace('bearer ', '')
        )
