from fastapi import APIRouter

from app.routes import auth, password, post, reply, user

routers = APIRouter()


def register(router, prefix, tags) -> None:
    routers.include_router(router=router, prefix=prefix, tags=tags)


register(auth.router, "", ["auth"])

register(user.router, "/users", ["users"])

register(password.router, "/password", ["password"])

register(post.router, "/posts", ["posts"])

register(reply.router, "/replies", ["replies"])
