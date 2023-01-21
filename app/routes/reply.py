from fastapi import APIRouter, Depends

from app.models.post import PostRequest, PostResponse
from app.models.user import ProfileModel
from app.security.session import session

from .controllers.reply_controller import ReplyController

router = APIRouter()

# PRIVATE ROUTES
@router.post(
    "/{postId}",
    response_model=PostResponse,
    response_model_exclude_none=True,
    status_code=201,
)
async def create_new_reply(
    postId: int,
    request: PostRequest,
    current_user: ProfileModel = Depends(session),
):
    return await ReplyController.create_reply(postId, request, current_user)


@router.post("/{replyId}/like", response_model_exclude_none=True, status_code=201)
async def add_like_on_reply(
    replyId: int,
    current_user: ProfileModel = Depends(session),
):
    return await ReplyController.add_like(replyId, current_user)


@router.patch("/{replyId}")
async def edit_reply(
    replyId: int,
    request: PostRequest,
    current_user: ProfileModel = Depends(session),
):
    return await ReplyController.edit_reply(replyId, request, current_user)


@router.delete("/{replyId}")
async def delete_reply(replyId: int, current_user: ProfileModel = Depends(session)):

    return await ReplyController.delete_reply(replyId, current_user)
