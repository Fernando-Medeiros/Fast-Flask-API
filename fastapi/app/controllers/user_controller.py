from fastapi import APIRouter, Form

from ..models.user import UserModel, UserRequest, UserResponse
from .decorators import post_user

router = APIRouter()

@router.post('/', response_model=UserResponse)
@post_user.post(UserModel)
async def create(request_model: UserRequest):
    pass


@router.post('/login')
@post_user.post_login(UserModel)
async def login(email: str = Form(...), password: str = Form(...)):
    pass
