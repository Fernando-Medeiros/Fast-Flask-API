from fastapi import APIRouter

from app.routes import auth, post, user

routers = APIRouter()


def register(router, prefix, tags) -> None:
    routers.include_router(router=router, prefix=prefix, tags=tags)


register(auth.router, "", ["auth"])
register(user.router, "/users", ["users"])
register(user.routerAuth, "/users", ["users-auth"])
register(post.router, "/posts", ["posts"])
register(post.routerAuth, "/posts", ["posts-auth"])
