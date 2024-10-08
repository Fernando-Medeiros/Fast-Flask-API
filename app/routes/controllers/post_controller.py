from app.models.post import LikeModel, PostModel, PostRequest
from app.models.user import ProfileModel
from app.security.backend import BackendDatabase


class PostController:
    backend = BackendDatabase

    @classmethod
    async def get_all(cls):
        return await cls.backend.get_all_order_by(PostModel, "-id")

    @classmethod
    async def get_post_by_id(cls, postId):
        return await cls.backend.get_or_404(PostModel, id=postId)

    @classmethod
    async def get_post_by_username(cls, username):
        user = await cls.backend.get_or_404(ProfileModel, username=username)
        return await cls.backend.get_all_filter_by(PostModel, author=user.id)

    @classmethod
    async def create_post(cls, request: PostRequest, current_user):
        data = request.dict()

        await cls.backend.create_or_400(PostModel, author=current_user.pk, **data)
        return {"detail": "Post created successfully"}

    @classmethod
    async def edit_post(cls, postId, request: PostRequest, current_user):
        data = request.dict()
        post = await cls.backend.get_or_404(
            PostModel, "Unauthorized", id=postId, author=current_user.id
        )
        await post.update(edit=True, **data)

        return {"detail": "Updated"}

    @classmethod
    async def delete_post(cls, postId, current_user):
        await cls.backend.delete_or_404(
            PostModel, "Unauthorized", id=postId, author=current_user.id
        )

        return {"detail": "Deleted"}

    @classmethod
    async def add_or_remove_like(cls, postId, current_user):
        post = await cls.backend.get_or_404(PostModel, id=postId)

        like = await cls.backend.get_or_none(
            LikeModel, post=postId, user=current_user.id
        )
        if like:
            await cls.backend.delete_or_404(LikeModel, id=like.id)
            return {"detail": "Like removed"}

        await cls.backend.create_or_400(
            LikeModel,
            user=current_user.pk,
            post=post.pk,
        )
        return {"detail": "Like added"}
