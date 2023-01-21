import pytest
from fastapi.testclient import TestClient

from app import app
from setup import conf_database_test
from tests.utils.client import CaseLogin
from tests.utils.post import CasePostCreate


class UrlToken:
    token = "/token"
    refresh = "/refresh"


class UrlUsers:
    create = "/users"
    delete = "/users"
    get_profiles = "/users"
    get_profile = "/users/"
    get_account = "/users/account/"
    update_profile = "/users/profile"
    update_avatar = "/users/avatar"
    update_birthday = "/users/birthday"
    update_account = "/users/account"


class UrlPassword:
    update = "/password"
    recover = "/password"
    reset = "/password/"


class UrlPosts:
    create = "/posts"
    update = "/posts/"
    delete = "/posts/"
    get_posts = "/posts"
    get_post_id = "/posts/"
    get_timeline = "/posts/timeline"
    get_posts_by_user = lambda username: f"/posts/{username}/posts"
    add_like = lambda postId: f"/posts/{postId}/like"


class UrlReply:
    create = "/replies/"
    update = "/replies/"
    delete = "/replies/"
    add_like = lambda replyId: f"/replies/{replyId}/like"


def client_authenticated(client):
    conf_database_test()
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
    conf_database_test()
    with TestClient(app()) as client:
        yield client


# Client with a user in the database
@pytest.fixture(scope="function")
def client_one():
    conf_database_test()
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
