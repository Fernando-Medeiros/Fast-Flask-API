from typing import List

from fastapi import APIRouter, Depends

from app.models.user import (
    RequestUpdate,
    UserModel,
    UserRequest,
    UserResponse,
    UserResponseAccountData,
)

from .controllers import user_controller
from .security.login_required import login_required

router = APIRouter()


# PULIC ROUTES
@router.get("", response_model=List[UserResponse])
async def get_list_with_all_users():

    return await user_controller.get_all_users()


@router.get("/{username}", response_model=UserResponse)
async def get_by_username(username: str):

    return await user_controller.get_by_username(username)


@router.post("", response_model=UserResponse, status_code=201)
async def new_account(request_model: UserRequest):

    return await user_controller.create_account(request_model)


# PRIVATE ROUTES
@router.patch("/update")
async def update_account(
    request_model: RequestUpdate, current_user: UserModel = Depends(login_required)
):
    return await user_controller.update_account(request_model, current_user)


@router.delete("/delete")
async def delete_account(current_user: UserModel = Depends(login_required)):

    return await user_controller.delete_account(current_user)


@router.get("/account/", response_model=UserResponseAccountData)
async def get_account_data(current_user: UserModel = Depends(login_required)):

    return await user_controller.get_account_data(current_user)
