import pytest
from fastapi.testclient import TestClient

from app import app
from setup import conf_database_test
from tests.utils.post import CaseCreate
from tests.utils.user import CaseLogin


class UrlToken:
    token = "/token"
    refresh = "/refresh"


class UrlUsers:
    account_create = "/users"
    account_update = "/users/update"
    account_delete = "/users/delete"
    account_data = "/users/account/"
    get_all = "/users"
    get_user = "/users/"
    pwd_update = "/users/password/update"
    pwd_recover = "/users/password/recover"
    pwd_reset = "/users/password/reset/"


class UrlPosts:
    create = "/posts"
    get_all = "/posts"
    get_post_id = "/posts/"
    get_posts_user = "/posts/user/"
    update = "/posts/"
    delete = "/posts/"


def client_authenticated(client):
    conf_database_test()
    case, post = CaseLogin(), CaseCreate()

    # Register new user
    client.post(UrlUsers.account_create, json=case.valid_user)

    # Get access token
    response = client.post(UrlToken.token, data=case.login, headers=case.content_type)

    # Set authorization in header
    token = response.json().get("access_token")
    client.headers["authorization"] = f"bearer {token}"

    # Create a new post
    client.post(UrlPosts.create, json=post.valid_content)


@pytest.fixture(scope="function")
def client():
    conf_database_test()
    with TestClient(app()) as client:
        yield client


# Client with a user in the database
@pytest.fixture(scope="function")
def client_one():
    conf_database_test()
    with TestClient(app()) as client:
        client.post(UrlUsers.account_create, json=CaseLogin.valid_user)
        yield client


# Client with an authenticated user
@pytest.fixture(scope="function")
def client_two_auth():
    with TestClient(app()) as client:
        client_authenticated(client)
        yield client


# Client with an authenticated user and a post to the database
@pytest.fixture(scope="function")
def client_three():
    with TestClient(app()) as client:
        client_authenticated(client)
        yield client
