from app.models import LikeModel, PostModel, ReplyModel
from app.repositories.backend import BackendDatabase
from app.requests import PostRequest


class ReplyController:
    repository = BackendDatabase

    @classmethod
    async def get_reply_by_id(cls, replyId) -> ReplyModel:

        return await cls.repository.get_or_404(ReplyModel, id=replyId)

    @classmethod
    async def get_replies_by_post_id(cls, postId) -> list[ReplyModel | None]:

        return await cls.repository.get_all_filter_by(ReplyModel, post=postId)

    @classmethod
    async def create_reply(cls, postId, request: PostRequest, current_user) -> None:
        data = request.dict()

        post = await cls.repository.get_or_404(PostModel, id=postId)

        await cls.repository.create_or_400(
            ReplyModel, post=post.pk, author=current_user.pk, **data
        )

    @classmethod
    async def edit_reply(cls, replyId, request: PostRequest, current_user) -> None:
        data = request.dict()

        reply = await cls.repository.get_or_404(
            ReplyModel, id=replyId, author=current_user.id
        )

        await reply.update(edit=True, **data)

    @classmethod
    async def delete_reply(cls, replyId, current_user) -> None:
        await cls.repository.delete_or_404(
            ReplyModel, id=replyId, author=current_user.id
        )

    @classmethod
    async def add_or_remove_like(cls, replyId, current_user) -> None:
        post = await cls.repository.get_or_404(ReplyModel, id=replyId)

        like = await cls.repository.get_or_none(
            LikeModel, reply=replyId, user=current_user.id
        )
        if like:
            await cls.repository.delete_or_404(LikeModel, id=like.id)
            return

        await cls.repository.create_or_400(
            LikeModel,
            user=current_user.pk,
            reply=post.pk,
        )
