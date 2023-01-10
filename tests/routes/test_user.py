import pytest
from fastapi.testclient import TestClient

from ..utils.user import CaseCreate

case = CaseCreate()


# POST CREATE ACCOUNT
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


# GET BY USERNAME WITHOUT USERS
@pytest.mark.user
def test_get_by_username_without_users(client: TestClient):
    response = client.get(f'/user/{"marciaSouza"}')
    
    assert response.status_code == 404


# GET ACCOUNT DATA (AUTH REQUIRED)
@pytest.mark.userAuth
def test_get_account_data(client_two_header_auth: TestClient):
    response = client_two_header_auth.get(f'/user/account-data/')
    context = response.json()

    assert response.status_code == 200
    assert issubclass(type(context['id']), int)
    assert issubclass(type(context['created_at']), str)


# GET ACCOUNT DATA (WITHOUT AUTH)
@pytest.mark.user
def test_get_account_data_without_auth(client_one: TestClient):
    response = client_one.get(f'/user/account-data/')

    assert response.status_code == 401


# UPDATE CONTENT (AUTH REQUIRED)
@pytest.mark.userAuth
def test_update_auth_user(client_two_header_auth: TestClient):
    to_update = case.get_one_valid_field('email')
    response = client_two_header_auth.patch(f'/user/', json=to_update)

    assert response.status_code == 200


# UPDATE INVALID CONTENT (AUTH REQUIRED)
@pytest.mark.userAuth
def test_update_auth_user_invalid_content(client_two_header_auth: TestClient):
    to_update = case.get_one_invalid_field('email')
    response = client_two_header_auth.patch(f'/user/', json=to_update)

    assert response.status_code == 400


# UPDATE VALID CONTENT (WITHOUT AUTH)
@pytest.mark.user
def test_update_without_auth_user(client_one: TestClient):
    to_update = case.get_one_valid_field('email')
    response = client_one.patch(f'/user/', json=to_update)

    assert response.status_code == 401


# UPDATE PASSWORD (AUTH REQUIRED)
@pytest.mark.userAuth
def test_update_password(client_two_header_auth: TestClient):
    to_update = case.get_one_valid_field('password')
    response = client_two_header_auth.patch(f'/user/update-password/', json=to_update)

    assert response.status_code == 200


# UPDATE INVALID PASSWORD (AUTH REQUIRED)
@pytest.mark.userAuth
def test_update_invalid_password(client_two_header_auth: TestClient):
    to_update = case.get_one_invalid_field('password')
    response = client_two_header_auth.patch(f'/user/update-password/', json=to_update)

    assert response.status_code == 400


# UPDATE PASSWORD (WITHOUT AUTH)
@pytest.mark.user
def test_update_password_without_auth_user(client_one: TestClient):
    to_update = case.get_one_valid_field('password')
    response = client_one.patch(f'/user/update-password/', json=to_update)

    assert response.status_code == 401


# DELETE (AUTH REQUIRED)
@pytest.mark.userAuth
def test_delete_auth_user(client_two_header_auth: TestClient):
    response = client_two_header_auth.delete(f'/user/')

    assert response.status_code == 200


# DELETE (WITHOUT AUTH)
@pytest.mark.userAuth
def test_delete_without_auth_user(client: TestClient):
    response = client.delete(f'/user/')

    assert response.status_code == 401
