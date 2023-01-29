from typing import List

import pytest

from tests.conftest import UrlPosts
from tests.utils.client import CaseLogin
from tests.utils.post import CasePostCreate, CasePostUpdate

post = CasePostCreate
post_update = CasePostUpdate


@pytest.mark.post
class TestPost:
    path = UrlPosts.create

    # (AUTH REQUIRED) - VALID
    def test_post_valid(self, client_two_auth):
        response = client_two_auth.post(self.path, json=post.valid_content)

        assert response.status_code == 201
        assert response.json().get("detail")

    # (AUTH REQUIRED) - INVALID
    def test_post_invalid(self, client_two_auth):
        response = client_two_auth.post(self.path, json=post.invalid_content)

        assert response.status_code == 400
        assert response.json().get("detail")

    # (WITHOUT AUTH) - INVALID
    def test_post_invalid_without_auth(self, client_one):
        response = client_one.post(self.path, json=post.invalid_content)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.post
class TestGet:
    username: str = CaseLogin.data["username"]

    path_all = UrlPosts.get_all
    path_id = UrlPosts.get_by_id
    path_user = UrlPosts.get_all_by_username(username)
    id = 1

    def test_get_all_posts(self, client_three):
        response = client_three.get(self.path_all)
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context), List)
        assert len(context) > 0

    def test_get_post_by_id(self, client_three):
        response = client_three.get("{}{}".format(self.path_id, self.id))

        assert response.status_code == 200
        assert response.json()["author"]["username"] == self.username

    def test_get_posts_by_username(self, client_three):
        response = client_three.get(self.path_user)

        assert response.status_code == 200
        assert issubclass(type(response.json()), list)
        assert issubclass(type(response.json()[0]["id"]), int)

    # (WITHOUT POSTS or USERS)
    def test_get_post_by_id_without_posts(self, client_one):
        response = client_one.get("{}{}".format(self.path_id, self.id))

        assert response.status_code == 404
        assert response.json().get("detail")

    def test_get_post_by_username_without_user(self, client):
        response = client.get(self.path_user)

        assert response.status_code == 404
        assert response.json().get("detail")


@pytest.mark.post
class TestUpdate:
    path = UrlPosts.update
    id = 1

    # (AUTH REQUIRED) - VALID
    def test_update_valid_content(self, client_three):
        response = client_three.patch(
            "{}{}".format(self.path, self.id), json=post_update.valid_content
        )

        assert response.status_code == 200
        assert response.json().get("detail")

    # (AUTH REQUIRED) - INVALID
    def test_update_invalid_content(self, client_three):
        response = client_three.patch(
            "{}{}".format(self.path, self.id), json=post_update.invalid_content
        )

        assert response.status_code == 400
        assert response.json().get("detail")


@pytest.mark.post
class TestDelete:
    path = UrlPosts.delete
    id = 1

    # (AUTH REQUIRED)
    def test_delete_post(self, client_three):
        f_response = client_three.delete("{}{}".format(self.path, self.id))
        s_response = client_three.delete("{}{}".format(self.path, self.id))

        assert f_response.status_code == 200
        assert f_response.json().get("detail")
        assert s_response.status_code == 404
        assert s_response.json().get("detail")
