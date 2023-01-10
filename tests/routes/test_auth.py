import pytest
from app.utils.token_jwt import DecodeTokenJwt

from fastapi.testclient import TestClient

from ..utils.user import CaseLogin

case = CaseLogin()

# LOGIN - TOKEN
@pytest.mark.token
def test_login_valid_user(client_one: TestClient):    
    response = client_one.post('/auth/token', data=case.login, headers=case.content_type)
    context = response.json()    
    
    assert response.status_code == 200
    assert [context[key] for key in case.headers]


# AUTHENTICATED CLIENT WITH BEARER
@pytest.mark.userAuth
def test_authenticated_client(client_two_header_auth: TestClient):
    assert DecodeTokenJwt().decode(
        client_two_header_auth.headers['Authorization'].replace('bearer ', '')
        )
