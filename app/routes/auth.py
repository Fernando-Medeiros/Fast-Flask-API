from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers import AuthController
from app.helpers import StatusOk
from app.responses import Token

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_with_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    resp = await AuthController.token(form_data)

    return StatusOk(resp)


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str = Form(...)):
    resp = await AuthController.refresh_token(refresh_token)

    return StatusOk(resp)
