from typing import List

from fastapi import APIRouter, Depends

from ..models.user import UserModel, UserRequest, UserResponse
from ..utils.login_required import login_required
from .decorators import user_controller

router = APIRouter()


@router.get('/', response_model=List[UserResponse])
async def list_users():
    ...


@router.get('/{username}', response_model=UserResponse)
async def get_by_username(username: str):
    ...


@router.post('/', response_model=UserResponse)
@user_controller.post(UserModel)
async def create_new_account(request_model: UserRequest):
    ...


@router.patch('/{id}')
@user_controller.patch(UserModel)
async def update_user(id: int, current_user: UserModel = Depends(login_required)):
    ...


@router.delete('/{id}')
@user_controller.delete(UserModel)
async def delete_user(id: int, current_user: UserModel = Depends(login_required)):
    ...