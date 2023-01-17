from typing import List

from fastapi import APIRouter, Depends, status

from app.models.post import PostRequest, PostResponse
from app.models.user import UserModel

from .controllers import post_controller
from .security.login_required import login_required

router = APIRouter()


# PUBLIC ROUTES
@router.get("", response_model=List[PostResponse])
async def list_posts():

    return await post_controller.get_all()


@router.get("/{id}", response_model=PostResponse)
async def get_post_by_id(id: int):

    return await post_controller.get_by_id(id)


@router.get("/user/{username}", response_model=List[PostResponse])
async def get_posts_by_username(username: str):

    return await post_controller.get_by_username(UserModel, username)


# PRIVATE ROUTES
@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    request_model: PostRequest, current_user: UserModel = Depends(login_required)
):
    return await post_controller.create(request_model, current_user)


@router.patch("/{id}", response_model=PostResponse)
async def edit_post(
    id: int,
    request_model: PostRequest,
    current_user: UserModel = Depends(login_required),
):
    return await post_controller.update(id, request_model, current_user)


@router.delete("/{id}")
async def delete_post(id: int, current_user: UserModel = Depends(login_required)):

    return await post_controller.delete(id, current_user)
