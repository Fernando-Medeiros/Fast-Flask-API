from fastapi.testclient import TestClient

from ..utils.user import TestUser

utils = TestUser()


def test_post_valid_user(client: TestClient) -> None:
    body = utils.valid_user()
    response = client.post('/user/', json=body)
    context = response.json()

    assert response.status_code == 200
    assert context['email'] == body['email']


def test_post_invalid_name(client: TestClient) -> None:
    body = utils.invalid_user('name')
    response = client.post('/user/', json=body)

    assert response.status_code == 400
    

def test_post_invalid_email(client: TestClient) -> None:
    body = utils.invalid_user('email')
    response = client.post('/user/', json=body)

    assert response.status_code == 400


def test_post_invalid_password(client: TestClient) -> None:
    body = utils.invalid_user('password')
    response = client.post('/user/', json=body)

    assert response.status_code == 400