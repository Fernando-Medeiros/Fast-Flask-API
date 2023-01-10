from fastapi import APIRouter

from .controllers import auth, post, user

router = APIRouter()

router.include_router(
    auth.router,
    prefix='/auth',
    tags=['Auth']
)

router.include_router(
    user.router,
    prefix='/user',
    tags=['User']
)

router.include_router(
    post.router,
    prefix='/post',
    tags=['Post']
)
