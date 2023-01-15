from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.token import RefreshToken, Token

from .controllers import auth_controller

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_with_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    return await auth_controller.token(form_data)


@router.post("/refresh_token", response_model=Token)
async def refresh_token(form_data: RefreshToken):

    return await auth_controller.refresh_token(form_data)
