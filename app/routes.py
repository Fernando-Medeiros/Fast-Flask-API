from fastapi import APIRouter

from .controllers import auth, post, user

routers = APIRouter()

routers.include_router(auth.router, prefix="", tags=["auth"])

routers.include_router(user.router, prefix="/users", tags=["users"])
routers.include_router(user.routerAuth, prefix="/users", tags=["users-auth"])

routers.include_router(post.router, prefix="/posts", tags=["posts"])
routers.include_router(post.routerAuth, prefix="/posts", tags=["posts-auth"])
