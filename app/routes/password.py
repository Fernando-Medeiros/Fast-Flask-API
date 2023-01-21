from fastapi import APIRouter, Depends, Form

from app.models.user import UserModel
from app.security.session import session

from .controllers.password_controller import PwdController

router = APIRouter()

# PUBLIC ROUTES
@router.post("")
async def send_recovery_email(email: str = Form(...)):

    return await PwdController.recover_password(email)


@router.patch("/{token}")
async def reset_password(
    token: str, password: str = Form(...), confirm: str = Form(...)
):
    return await PwdController.reset_password(token, password, confirm)


# PRIVATE ROUTES
@router.patch("")
async def update_password(
    password: str = Form(...),
    current_user: UserModel = Depends(session),
):
    return await PwdController.update_password(password, current_user)
