from fastapi import APIRouter, Depends, Form

from app.models.user import RequestRecoverPassword, RequestUpdatePassword, UserModel

from .controllers import password_controller
from .security.login_required import login_required

router = APIRouter()

# PUBLIC ROUTES
@router.post("/recover")
async def recover_password(request_model: RequestRecoverPassword):

    return await password_controller.recover_password(request_model)


@router.patch("/reset/{token}")
async def reset_password(
    token: str, password: str = Form(...), confirm: str = Form(...)
):

    return await password_controller.reset_password(token, password, confirm)


# PRIVATE ROUTES
@router.patch("/update")
async def update_password(
    request_model: RequestUpdatePassword,
    current_user: UserModel = Depends(login_required),
):
    return await password_controller.update_password(request_model, current_user)
