from typing import List

from fastapi import APIRouter, Depends

from app.controllers import PostController
from app.helpers import StatusCreated, StatusOk, StatusOkNoContent
from app.models import ProfileModel
from app.requests import PostRequest
from app.responses import PostResponse
from app.security.session import session

router = APIRouter()


# PUBLIC ROUTES
@router.get(
    "",
    response_model=List[PostResponse],
    response_model_exclude_unset=True,
)
async def list_all_posts():
    resp = await PostController.get_all()

    return StatusOk(resp)


@router.get(
    "/{postId}",
    response_model=PostResponse,
    response_model_exclude_unset=True,
)
async def get_post_by_id(postId: int):
    resp = await PostController.get_post_by_id(postId)

    return StatusOk(resp)


@router.get(
    "/{username}/posts",
    response_model=List[PostResponse],
    response_model_exclude_unset=True,
)
async def get_posts_by_username(username: str):
    resp = await PostController.get_post_by_username(username)

    return StatusOk(resp)


# PRIVATE ROUTES
@router.post("")
async def create_new_post(
    request: PostRequest, current_user: ProfileModel = Depends(session)
):
    resp = await PostController.create_post(request, current_user)

    return StatusCreated(resp)


@router.post("/{postId}/like")
async def add_like_on_post(
    postId: int,
    current_user: ProfileModel = Depends(session),
):
    resp = await PostController.add_or_remove_like(postId, current_user)

    return StatusCreated(resp)


@router.patch("/{postId}")
async def edit_post(
    postId: int,
    request: PostRequest,
    current_user: ProfileModel = Depends(session),
):
    resp = await PostController.edit_post(postId, request, current_user)

    return StatusOkNoContent(resp)


@router.delete("/{postId}")
async def delete_post(postId: int, current_user: ProfileModel = Depends(session)):
    resp = await PostController.delete_post(postId, current_user)

    return StatusOkNoContent(resp)
