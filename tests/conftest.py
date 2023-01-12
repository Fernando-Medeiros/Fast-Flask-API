import pytest
from fastapi.testclient import TestClient

from app import app
from setup import conf_database_test

from .utils.post import CaseCreate
from .utils.user import CaseLogin


def client_authenticated():
    conf_database_test()
    client = TestClient(app())
    client.post("api/users", json=CaseLogin().valid_user)

    response = client.post(
        "/api/token", data=CaseLogin().login, headers=CaseLogin().content_type
    )
    token = response.json()["access_token"]
    client.headers["Authorization"] = f"bearer {token}"
    return client


@pytest.fixture(scope="function")
def client():
    conf_database_test()
    with TestClient(app()) as client:
        yield client


# Client with a user in the database
@pytest.fixture(scope="function")
def client_one():
    conf_database_test()
    client = TestClient(app())
    client.post("api/users", json=CaseLogin().valid_user)
    return client


# Client with an authenticated user
@pytest.fixture(scope="function")
def client_two_header_auth():
    client = client_authenticated()
    return client


# Client with an authenticated user and a post to the database
@pytest.fixture(scope="function")
def client_three():
    client = client_authenticated()
    client.post("/api/posts", json=CaseCreate().valid_content)
    return client
