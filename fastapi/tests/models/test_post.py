import asyncio

import pytest
from app.models.post import (PostModel, PostRequest, PostRequestPatch,
                             PostResponse)
from tests.utils.post import CaseCreate

from fastapi import HTTPException

case = CaseCreate()


# PostModel - Valid content
@pytest.mark.postModel
def test_model_valid_postmodel():
    attr: dict = case.valid_model_content
    post = PostModel(**attr)
    
    assert [post.dict()[key] for key in attr]


# PostModel - Invalid content
@pytest.mark.postModel
def test_model_invalid_post_content():
    with pytest.raises(HTTPException):
        attr: dict = case.invalid_content
        post = PostModel(**attr)


# Create Post
@pytest.mark.postModel
def test_model_create_post():
    attr: dict = case.valid_content
    post = PostModel(**attr)
    event = asyncio.new_event_loop()
    
    assert event.run_until_complete(post.save()) == post


# Delete Post
@pytest.mark.postModel
def test_model_delete_post():
    event = asyncio.new_event_loop()
    post = event.run_until_complete(PostModel.objects.first())

    id: int = event.run_until_complete(post.delete())
    
    with pytest.raises(Exception):
        event.run_until_complete(PostModel.objects.get(id=id))


# PostRequest
@pytest.mark.postModel
@pytest.mark.postModelRequest
def test_model_post_request():
    attr: dict = case.valid_model_content
    post = PostRequest(**attr)

    assert post.content == attr['content']


# PostResponse
@pytest.mark.postModel
@pytest.mark.postModelResponse
def test_model_post_response():
    attr: dict = case.valid_model_content
    request = PostRequest(**attr)
    model = PostModel(**request.dict())
    response = PostResponse(**model.dict())
    
    assert [response.dict()[key] for key in attr if key not in ['author']]
