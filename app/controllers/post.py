from typing import List

from fastapi import APIRouter, Depends, status

from ..models.post import PostRequest, PostResponse
from ..models.user import UserModel
from ..utils.login_required import login_required
from .backend import post_controller

router = APIRouter()
routerAuth = APIRouter()


@router.get("", response_model=List[PostResponse])
async def list_posts():

    return await post_controller.get_all()


@router.get("/{id}", response_model=PostResponse)
async def get_post_by_id(id: int):

    return await post_controller.get_by_id(id)


@router.get("/user/{username}", response_model=List[PostResponse])
async def get_posts_by_username(username: str):

    return await post_controller.get_by_username(UserModel, username)


@routerAuth.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    request_model: PostRequest, current_user: UserModel = Depends(login_required)
):
    return await post_controller.create(request_model, current_user)


@routerAuth.patch("/{id}", response_model=PostResponse)
async def edit_post(
    id: int,
    request_model: PostRequest,
    current_user: UserModel = Depends(login_required),
):
    return await post_controller.update(id, request_model, current_user)


@routerAuth.delete("/{id}")
async def delete_post(id: int, current_user: UserModel = Depends(login_required)):

    return await post_controller.delete(id, current_user)
