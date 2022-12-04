from app.utils.token_jwt import DecodeTokenJwt

from fastapi.testclient import TestClient

from ..utils.user import CaseCreate, CaseLogin

post_utils = CaseCreate()
login_utils = CaseLogin()

# CREATE
def test_post_valid_user(client: TestClient) -> None:
    body = post_utils.valid_user
    response = client.post('/auth/', json=body)
    context = response.json()

    assert response.status_code == 200
    assert context['email'] == body['email']


def test_post_invalid_name(client: TestClient) -> None:
    body = post_utils.invalid_user('name')
    response = client.post('/auth/', json=body)

    assert response.status_code == 400
    

def test_post_invalid_email(client: TestClient) -> None:
    body = post_utils.invalid_user('email')
    response = client.post('/auth/', json=body)

    assert response.status_code == 400


def test_post_invalid_password(client: TestClient) -> None:
    body = post_utils.invalid_user('password')
    response = client.post('/auth/', json=body)

    assert response.status_code == 400


# LOGIN
def test_login_valid_user(client: TestClient) -> None:
    body = login_utils.valid_user
    client.post('/auth/', json=body)
    
    response = client.post('/auth/login', data=body)
    context = response.json()

    token = DecodeTokenJwt().decode(context['access_token'])

    assert response.status_code == 200
    assert context['access_token'] and context['token_type']
    assert token['id']


# AUTHENTICATED USER WITH BEARER AUTH
def test_authenticated_user(client_auth: TestClient) -> None:
    assert DecodeTokenJwt().decode(
        client_auth.headers['Authorization'].replace('bearer ', '')
        )