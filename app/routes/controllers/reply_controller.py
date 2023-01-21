from app.models.post import LikeModel, PostModel, PostRequest, ReplyModel
from app.security.backend import BackendDatabase


class ReplyController:
    backend = BackendDatabase

    @classmethod
    async def create_reply(cls, postId, request: PostRequest, current_user):
        data = request.dict()
        post = await cls.backend.get_or_404(PostModel, id=postId)

        return await cls.backend.create_or_400(
            ReplyModel, post=post.pk, author=current_user.pk, **data
        )

    @classmethod
    async def edit_reply(cls, replyId, request: PostRequest, current_user):
        data = request.dict()
        reply = await cls.backend.get_or_404(
            ReplyModel, id=replyId, author=current_user.id
        )
        await reply.update(edit=True, **data)

        return {"detail": "Updated"}

    @classmethod
    async def delete_reply(cls, replyId, current_user):
        await cls.backend.delete_or_404(ReplyModel, id=replyId, author=current_user.id)

        return {"detail": "Deleted"}

    @classmethod
    async def add_like(cls, replyId, current_user):
        post = await cls.backend.get_or_404(ReplyModel, id=replyId)

        await cls.backend.create_or_400(
            LikeModel,
            user=current_user.pk,
            reply=post.pk,
        )
        return {"detail": "Like added"}
