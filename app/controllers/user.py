from typing import List

from fastapi import APIRouter, Depends, status

from ..models.user import (
    UserModel,
    UserRequest,
    UserRequestPatch,
    UserRequestUpdatePassword,
    UserResponse,
    UserResponseAccountData,
)
from ..utils.login_required import login_required
from .backend import user_controller

router = APIRouter()
routerAuth = APIRouter()


@router.get("", response_model=List[UserResponse])
async def get_list_with_all_users():

    return await user_controller.get_all()


@router.get("/{username}", response_model=UserResponse)
async def get_user_by_username(username: str):

    return await user_controller.get_by_username(username)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_new_account(request_model: UserRequest):

    return await user_controller.create_account(request_model)


@routerAuth.patch("", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    request_model: UserRequestPatch, current_user: UserModel = Depends(login_required)
):
    return await user_controller.update_user(request_model, current_user)


@routerAuth.patch("/update_password")
async def update_password(
    request_model: UserRequestUpdatePassword,
    current_user: UserModel = Depends(login_required),
):
    return await user_controller.update_password(request_model, current_user)


@routerAuth.delete("")
async def delete_account(current_user: UserModel = Depends(login_required)):

    return await user_controller.delete(current_user)


@routerAuth.get("/account_data/", response_model=UserResponseAccountData)
async def get_account_data(current_user: UserModel = Depends(login_required)):

    return await user_controller.get_account_data(current_user)
