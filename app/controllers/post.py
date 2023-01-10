from typing import List

from fastapi import APIRouter, Depends

from ..models.post import (PostModel, PostRequest, PostRequestPatch,
                           PostResponse)
from ..models.user import UserModel
from ..utils.login_required import login_required
from .decorators import post_controller

router = APIRouter()


@router.get('/', response_model=List[PostResponse])
@post_controller.get_all(PostModel)
async def list_posts():
    ...


@router.get('/id/{id}', response_model=PostResponse)
@post_controller.get_by_id(PostModel)
async def get_post_by_id(id: int):
    ...


@router.get('/username/{username}' ,response_model=List[PostResponse])
@post_controller.get_by_username(UserModel)
async def get_post_by_username(username: str):
    ...


@router.post('/', response_model=PostResponse)
@post_controller.post(PostModel)
async def create_post(
    request_model: PostRequest,
    current_user: UserModel = Depends(login_required)):
    ...


@router.patch('/{id}', response_model=PostResponse)
@post_controller.patch(PostModel)
async def edit_post(
    id: int,
    request_model: PostRequestPatch,
    current_user: UserModel = Depends(login_required)):
    ...


@router.delete('/{id}')
@post_controller.delete(PostModel)
async def delete_post(
    id: int,
    current_user: UserModel = Depends(login_required)):
    ...
