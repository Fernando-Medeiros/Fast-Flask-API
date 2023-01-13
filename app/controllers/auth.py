from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.token import RefreshToken, Token
from ..models.user import UserModel
from .decorators import auth_controller

router = APIRouter()


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    return await auth_controller.post_token(UserModel, form_data)


@router.post("/refresh_token")
async def refresh_token():

    return "Route will be implemented after finalizing the posts route"
