from typing import List

import pytest

from tests.conftest import UrlReply
from tests.utils.post import CasePostCreate, CasePostUpdate

post = CasePostCreate
post_update = CasePostUpdate


@pytest.mark.reply
class TestPost:
    path = "{}{}".format(UrlReply.create, 1)

    # (AUTH REQUIRED) - VALID
    def test_reply_valid(self, client_two_auth):
        response = client_two_auth.post(self.path, json=post.valid_content)

        assert response.status_code == 201

    # (AUTH REQUIRED) - INVALID
    def test_reply_invalid(self, client_two_auth):
        response = client_two_auth.post(self.path, json=post.invalid_content)

        assert response.status_code == 400
        assert response.json().get("detail")

    # (WITHOUT AUTH)
    def test_reply_invalid_without_auth(self, client_one):
        response = client_one.post(self.path, json=post.valid_content)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.reply
class TestGet:
    path_all = UrlReply.get_all_by_post_id(1)
    path_id = "{}{}".format(UrlReply.get_by_id, 1)

    def test_get_all_replies_by_post_id(self, client_three):
        response = client_three.get(self.path_all)
        context = response.json()

        assert response.status_code == 200
        assert issubclass(type(context), List)
        assert len(context) > 0

    def test_get_reply_by_id(self, client_three):
        response = client_three.get(self.path_id)

        assert response.status_code == 200
        assert response.json()

    # (WITHOUT USERS, POSTS AND REPLIES)
    def test_get_reply_by_id_without_posts(self, client_one):
        response = client_one.get(self.path_id)

        assert response.status_code == 404
        assert response.json().get("detail")


@pytest.mark.reply
class TestUpdate:
    path = "{}{}".format(UrlReply.update, 1)

    # (AUTH REQUIRED) - VALID
    def test_update_valid_content(self, client_three):
        response = client_three.patch(self.path, json=post_update.valid_content)

        assert response.status_code == 204

    # (AUTH REQUIRED) - INVALID
    def test_update_invalid_content(self, client_three):
        response = client_three.patch(self.path, json=post_update.invalid_content)

        assert response.status_code == 400
        assert response.json().get("detail")

    # (WITHOUT AUTH)
    def test_update_without_auth(self, client_one):
        response = client_one.patch(self.path, json=post_update.invalid_content)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.reply
class TestLike:
    path = UrlReply.add_like(1)
    path_invalid = UrlReply.add_like(5)

    # (AUTH REQUIRED)
    def test_add_like(self, client_three):
        response = client_three.post(self.path, json=post_update.valid_content)

        assert response.status_code == 201

    # (WITHOUT REPLY)
    def test_add_like_without_reply(self, client_three):
        response = client_three.post(self.path_invalid, json=post_update.valid_content)

        assert response.status_code == 404
        assert response.json().get("detail")

    # (WITHOUT AUTH)
    def test_add_like_without_auth(self, client_one):
        response = client_one.post(self.path, json=post_update.valid_content)

        assert response.status_code == 401
        assert response.json().get("detail")


@pytest.mark.reply
class TestDelete:
    path = "{}{}".format(UrlReply.delete, 1)

    # (AUTH REQUIRED)
    def test_delete_reply(self, client_three):
        f_response = client_three.delete(self.path)

        assert f_response.status_code == 204

        # (WITHOUT REPLY)
        s_response = client_three.delete(self.path)

        assert s_response.status_code == 404
        assert s_response.json().get("detail")

    # (WITHOUT AUTH)
    def test_delete_without_auth(self, client_one):
        response = client_one.delete(self.path)

        assert response.status_code == 401
        assert response.json().get("detail")
