from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.models.token import RefreshToken, Token

from .controllers.auth_controller import AuthController

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_with_access_token(form_data: OAuth2PasswordRequestForm = Depends()):

    return await AuthController.token(form_data)


@router.post("/refresh", response_model=Token)
async def refresh_token(form_data: RefreshToken):

    return await AuthController.refresh_token(form_data)
