from typing import List

from fastapi import APIRouter, Depends

from app.models.post import PostRequest, PostResponse
from app.models.user import ProfileModel
from app.security.session import session

from .controllers.reply_controller import ReplyController

router = APIRouter()


# PUBLIC ROUTES
@router.get(
    "/{replyId}",
    response_model=PostResponse,
    response_model_exclude_unset=True,
)
async def get_reply_by_id(replyId: int):
    return await ReplyController.get_reply_by_id(replyId)


@router.get(
    "/{postId}/replies",
    response_model=List[PostResponse],
    response_model_exclude_unset=True,
)
async def get_replies_by_post_id(postId: int):
    return await ReplyController.get_replies_by_post_id(postId)


# PRIVATE ROUTES
@router.post(
    "/{postId}",
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
async def add_or_remove_like(
    replyId: int,
    current_user: ProfileModel = Depends(session),
):
    return await ReplyController.add_or_remove_like(replyId, current_user)


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
