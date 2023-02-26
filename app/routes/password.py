from fastapi import APIRouter, Depends, Form

from app.controllers import PwdController
from app.helpers import StatusOk, StatusOkNoContent
from app.models.user import UserModel
from app.security.session import session

router = APIRouter()

# PUBLIC ROUTES
@router.post("")
async def send_recovery_email(email: str = Form(...)):
    resp = await PwdController.recover_password(email)

    return StatusOk(resp)


@router.patch("/{token}")
async def reset_password(
    token: str, password: str = Form(...), confirm: str = Form(...)
):
    resp = await PwdController.reset_password(token, password, confirm)

    return StatusOkNoContent(resp)


# PRIVATE ROUTES
@router.patch("")
async def update_password(
    password: str = Form(...),
    current_user: UserModel = Depends(session),
):
    resp = await PwdController.update_password(password, current_user)

    return StatusOkNoContent(resp)
