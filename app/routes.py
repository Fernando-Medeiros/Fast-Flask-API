from fastapi import APIRouter

from .controllers import auth, post, user

router = APIRouter()

router.include_router(auth.router, prefix="", tags=["auth"])

router.include_router(user.router, prefix="/users", tags=["users"])

router.include_router(post.router, prefix="/posts", tags=["posts"])
