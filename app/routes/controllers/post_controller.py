from datetime import datetime

from fastapi import HTTPException, status

from app.models.post import PostModel

model = PostModel


async def get_all():
    return await model.objects.all()


async def get_by_id(id):
    post = await model.objects.get_or_none(id=id)
    if post:
        return post

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Id not found")


async def get_by_username(model, username):
    entity = await model.objects.get_or_none(username=username)
    if entity:
        posts = await entity.posts.all()
        return posts

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Username not found")


async def update(id, request_model, current_user):
    post = await current_user.posts.get_or_none(id=id)

    if post:
        updates = request_model.dict(exclude_unset=True)
        return await post.update(**updates)


async def create(request_model, current_user):
    if current_user.id:
        data = request_model.dict(exclude_unset=True)
        post = model(
            author=current_user,
            date=datetime.today().date(),
            time=datetime.today().time(),
            **data
        )
        return await post.save()


async def delete(id, current_user):
    await model.objects.delete(id=id, author=current_user.id)

    if await model.objects.get_or_none(id=id, author=current_user.id) is None:
        return {"detail": "Post deleted"}

    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Post cannot be found")
