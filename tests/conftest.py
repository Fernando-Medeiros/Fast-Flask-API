import os

import pytest
from fastapi.testclient import TestClient

os.environ["ENV"] = "TEST"

from app import app
from setup import build_database_test
from tests.utils.client import CaseLogin
from tests.utils.post import CasePostCreate

_v_ = "api/v1/"


class UrlToken:
    token = _v_ + "token"
    refresh = _v_ + "refresh"


class UrlUsers:
    create = _v_ + "users"
    delete = _v_ + "users"
    get_profiles = _v_ + "users"
    get_profile = _v_ + "users/"
    get_account = _v_ + "users/account/"
    update_profile = _v_ + "users/profile"
    update_avatar = _v_ + "users/avatar"
    update_birthday = _v_ + "users/birthday"
    update_account = _v_ + "users/account"


class UrlPassword:
    update = _v_ + "password"
    recover = _v_ + "password"
    reset = _v_ + "password/"


class UrlPosts:
    create = _v_ + "posts"
    update = _v_ + "posts/"
    delete = _v_ + "posts/"
    get_all = _v_ + "posts"
    get_by_id = _v_ + "posts/"
    get_all_by_username = lambda username: f"{_v_}posts/{username}/posts"
    add_like = lambda postId: f"{_v_}posts/{postId}/like"


class UrlReply:
    create = _v_ + "replies/"
    update = _v_ + "replies/"
    delete = _v_ + "replies/"
    get_by_id = _v_ + "replies/"
    get_all_by_post_id = lambda postId: f"{_v_}replies/{postId}/replies"
    add_like = lambda replyId: f"{_v_}replies/{replyId}/like"


def client_authenticated(client):
    build_database_test()
    case, post = CaseLogin(), CasePostCreate()

    # Register new user
    client.post(UrlUsers.create, json=case.data)

    # Get access token
    response = client.post(UrlToken.token, data=case.login, headers=case.content_type)

    # Set authorization in header
    token = response.json().get("access_token")
    client.headers["authorization"] = f"bearer {token}"

    # Create a new post
    client.post(UrlPosts.create, json=post.valid_content)


@pytest.fixture(scope="function")
def client():
    build_database_test()
    with TestClient(app()) as client:
        yield client


# Client with a user in the database
@pytest.fixture(scope="function")
def client_one():
    build_database_test()
    with TestClient(app()) as client:
        client.post(UrlUsers.create, json=CaseLogin.data)
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
