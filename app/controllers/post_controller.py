from app.models import LikeModel, PostModel, ProfileModel
from app.repositories.backend import BackendDatabase
from app.requests import PostRequest


class PostController:
    repository = BackendDatabase

    @classmethod
    async def get_all(cls) -> list[PostModel]:
        return await cls.repository.get_all_order_by(PostModel, "-id")

    @classmethod
    async def get_post_by_id(cls, postId) -> PostModel | None:
        return await cls.repository.get_or_404(PostModel, id=postId)

    @classmethod
    async def get_post_by_username(cls, username) -> list[PostModel | None]:
        user = await cls.repository.get_or_404(ProfileModel, username=username)

        return await cls.repository.get_all_filter_by(PostModel, author=user.id)

    @classmethod
    async def create_post(cls, request: PostRequest, current_user) -> None:
        data = request.dict()

        await cls.repository.create_or_400(PostModel, author=current_user.pk, **data)

    @classmethod
    async def edit_post(cls, postId, request: PostRequest, current_user) -> None:
        data = request.dict()

        post = await cls.repository.get_or_404(
            PostModel, "Unauthorized", id=postId, author=current_user.id
        )

        await post.update(edit=True, **data)

    @classmethod
    async def delete_post(cls, postId, current_user) -> None:
        await cls.repository.delete_or_404(
            PostModel, "Unauthorized", id=postId, author=current_user.id
        )

    @classmethod
    async def add_or_remove_like(cls, postId, current_user) -> None:
        post = await cls.repository.get_or_404(PostModel, id=postId)

        like = await cls.repository.get_or_none(
            LikeModel, post=postId, user=current_user.id
        )

        if like:
            await cls.repository.delete_or_404(LikeModel, id=like.id)
            return

        await cls.repository.create_or_400(
            LikeModel,
            user=current_user.pk,
            post=post.pk,
        )
