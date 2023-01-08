from typing import List

from fastapi import APIRouter, Depends

from ..models.user import (UserModel, UserRequest, UserRequestPatch,
                           UserResponse)
from ..utils.login_required import login_required
from .decorators import user_controller

router = APIRouter()


@router.get('/', response_model=List[UserResponse])
@user_controller.get_all(UserModel)
async def get_list_users():
    ...


@router.get('/{username}', response_model=UserResponse)
@user_controller.get_by_username(UserModel)
async def get_by_username(username: str):
    ...


@router.post('/', response_model=UserResponse)
@user_controller.post(UserModel)
async def create_new_account(request_model: UserRequest):
    ...


@router.patch('/')
@user_controller.patch(UserModel)
async def update_user(
    request_model: UserRequestPatch,
    current_user: UserModel = Depends(login_required)):
    ...


@router.delete('/')
@user_controller.delete(UserModel)
async def delete_account(
    current_user: UserModel = Depends(login_required)):
    ...
