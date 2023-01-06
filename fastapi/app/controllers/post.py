from fastapi import APIRouter, Depends

from ..models.user import UserModel
from ..utils.login_required import login_required

router = APIRouter()


@router.get('/')
async def list_posts():
    ...


@router.get('/{post_id}')
async def get_by_post_id(post_id: int):
    ...


@router.get('/user/{username}')
async def get_by_username(username: str):
    ...


@router.post('/')
async def create_post(current_user: UserModel = Depends(login_required)):
    ...


@router.delete('/{id}')
async def delete_post(id: int, current_user: UserModel = Depends(login_required)):
    ...
