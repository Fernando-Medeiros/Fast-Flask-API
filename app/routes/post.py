from typing import List

from fastapi import APIRouter, Depends

from app.models.post import PostRequest, PostResponse
from app.models.user import ProfileModel
from app.security.session import session

from .controllers.post_controller import PostController

router = APIRouter()


# PUBLIC ROUTES
@router.get(
    "",
    response_model=List[PostResponse],
    response_model_exclude_unset=True,
)
async def list_all_posts():
    return await PostController.get_all()


@router.get(
    "/{postId}",
    response_model=PostResponse,
    response_model_exclude_unset=True,
)
async def get_post_by_id(postId: int):
    return await PostController.get_post_by_id(postId)


@router.get(
    "/{username}/posts",
    response_model=List[PostResponse],
    response_model_exclude_unset=True,
)
async def get_posts_by_username(username: str):
    return await PostController.get_post_by_username(username)


# PRIVATE ROUTES
@router.post("", status_code=201)
async def create_new_post(
    request: PostRequest, current_user: ProfileModel = Depends(session)
):
    return await PostController.create_post(request, current_user)


@router.post("/{postId}/like", status_code=201)
async def add_like_on_post(
    postId: int,
    current_user: ProfileModel = Depends(session),
):
    return await PostController.add_or_remove_like(postId, current_user)


@router.patch("/{postId}")
async def edit_post(
    postId: int,
    request: PostRequest,
    current_user: ProfileModel = Depends(session),
):
    return await PostController.edit_post(postId, request, current_user)


@router.delete("/{postId}")
async def delete_post(postId: int, current_user: ProfileModel = Depends(session)):

    return await PostController.delete_post(postId, current_user)
