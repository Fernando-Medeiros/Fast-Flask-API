import pytest

from fastapi.testclient import TestClient

from ..utils.user import CaseCreate

case = CaseCreate()


# POST VALID
@pytest.mark.user
def test_post_valid_user(client: TestClient):
    body = case.valid_user
    response = client.post('/user/', json=body)
    context = response.json()

    assert response.status_code == 200
    assert context['email'] == body['email']


# POST INVALID FIRST_NAME
@pytest.mark.user
def test_post_invalid_name(client: TestClient):
    body = case.invalid_user('first_name')
    response = client.post('/user/', json=body)

    assert response.status_code == 400
    

# POST INVALID EMAIL
@pytest.mark.user
def test_post_invalid_email(client: TestClient):
    body = case.invalid_user('email')
    response = client.post('/user/', json=body)

    assert response.status_code == 400


# POST INVALID PASSWORD
@pytest.mark.user
def test_post_invalid_password(client: TestClient):
    body = case.invalid_user('password')
    response = client.post('/user/', json=body)
    
    assert response.status_code == 400


# GET ALL
@pytest.mark.user
def test_get_all_users(client_one: TestClient):
    response = client_one.get('/user')
    context = response.json()

    assert response.status_code == 200
    assert issubclass(type(context), list)
    assert context[0]


# GET BY USERNAME
@pytest.mark.user
def test_get_by_username(client_one: TestClient):
    response = client_one.get(f'/user/{"marciaSouza"}')
    context = response.json()

    assert response.status_code == 200
    assert issubclass(type(context['id']), int)


# UPDATE (AUTH Required)
@pytest.mark.userAuth
def test_update_auth_user(client_two_header_auth: TestClient):
    to_update = {'email': 'newemail@hotmail.com'}
    response = client_two_header_auth.patch(f'/user/', json=to_update)

    assert response.status_code == 200


# DELETE (AUTH Required)
@pytest.mark.userAuth
def test_delete_auth_user(client_two_header_auth: TestClient):
    response = client_two_header_auth.delete(f'/user/')

    assert response.status_code == 200