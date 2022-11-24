from fastapi import APIRouter

from ..models.user import UserModel, UserRequest, UserResponse
from .decorators import post_user

router = APIRouter()

@router.post('/', response_model=UserResponse)
@post_user.post(UserModel)
async def create(request_model: UserRequest):
    pass