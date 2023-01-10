from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..models.token import RefreshToken, Token
from ..models.user import UserModel
from .decorators import auth_controller

router = APIRouter()


@router.post('/token', response_model=Token)
@auth_controller.post_token(UserModel)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    ...


@router.post('/refresh-token', response_model=RefreshToken)
async def refresh_token():
    ...
