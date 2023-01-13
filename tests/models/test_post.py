import asyncio
from datetime import datetime

import pytest
from fastapi import HTTPException

from app.models.post import PostModel, PostRequest, PostRequestPatch, PostResponse
from tests.utils.post import CaseCreate

case = CaseCreate()
event = asyncio.new_event_loop()


@pytest.mark.postModel
class TestPostModel:
    def test_valid_postmodel(self):
        data: dict = case.valid_content
        post = PostModel(**data).dict()

        assert [post[key] for key in data]

    def test_invalid_postmodel(self):
        with pytest.raises(HTTPException):
            data: dict = case.invalid_content
            PostModel(**data)

    def test_create_post(self):
        data: dict = case.valid_content
        post = PostModel(**data)

        assert event.run_until_complete(post.save()) == post

    def test_delete_post(self):
        post = event.run_until_complete(PostModel.objects.first())

        id: int = event.run_until_complete(post.delete())

        with pytest.raises(Exception):
            event.run_until_complete(PostModel.objects.get(id=id))


@pytest.mark.postModelRequest
class TestPostRequest:
    def test_post_request(self):
        data: dict = case.valid_content
        post = PostRequest(**data)

        assert post.content == data["content"]


@pytest.mark.postModelResponse
class TestPostResponse:
    def test_post_response(self):
        data: dict = case.valid_content
        request = PostRequest(**data).dict()
        model = PostModel(
            id=1, date=datetime.today().date(), time=datetime.today().time(), **request
        ).dict()
        response = PostResponse(**model).dict()

        assert [model[key] for key in response]

    # PostRequestPatch
