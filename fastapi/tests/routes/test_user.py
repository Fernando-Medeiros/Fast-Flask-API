import asyncio

import pytest

from fastapi.testclient import TestClient

from ..utils.user import CaseCreate

post_utils = CaseCreate()


# POST
@pytest.mark.userDefault
def test_post_valid_user(client: TestClient):
    body = post_utils.valid_user
    response = client.post('/user/', json=body)
    context = response.json()

    assert response.status_code == 200
    assert context['email'] == body['email']


@pytest.mark.userDefault
def test_post_invalid_name(client: TestClient):
    body = post_utils.invalid_user('name')
    response = client.post('/user/', json=body)

    assert response.status_code == 400
    

@pytest.mark.userDefault
def test_post_invalid_email(client: TestClient):
    body = post_utils.invalid_user('email')
    response = client.post('/user/', json=body)

    assert response.status_code == 400


@pytest.mark.userDefault
def test_post_invalid_password(client: TestClient):
    body = post_utils.invalid_user('password')
    response = client.post('/user/', json=body)
    
    assert response.status_code == 400


# GET ALL

# GET BY USERNAME

# UPDATE (AUTH Required)
@pytest.mark.userAuth
def test_update_auth_user(client_auth: TestClient):
    to_update = {}
    response = client_auth.patch(f'/user/{1}', json=to_update)
    context = response.json()

    assert response.status_code == 200


# DELETE (AUTH Required)
@pytest.mark.userAuth
def test_delete_auth_user(client_auth: TestClient):
    response = client_auth.delete(f'/user/{1}')

    assert response.status_code == 200