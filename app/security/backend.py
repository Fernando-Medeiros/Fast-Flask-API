from typing import List

from fastapi import HTTPException


class BackendDatabase:
    @staticmethod
    async def get_or_none(model, **kwargs):
        return await model.objects.get_or_none(**kwargs)

    @staticmethod
    async def get_all_order_by(model, column: str) -> List:
        result = await model.objects.order_by(column).all()
        return [await object.load_all() for object in result]

    @staticmethod
    async def get_all_filter_by(model, **kwargs) -> List:
        result = await model.objects.filter(**kwargs).all()
        return [await object.load_all() for object in result]

    @staticmethod
    async def get_or_404(model, detail: str = "Could not find", **kwargs):
        try:
            result = await model.objects.get(**kwargs)
            return await result.load_all()
        except:
            raise HTTPException(404, detail)

    @staticmethod
    async def create_or_400(model, detail: str = "Invalid data", **kwargs):
        try:
            return await model.objects.create(**kwargs)
        except:
            raise HTTPException(400, detail)

    @staticmethod
    async def delete_or_404(model, detail: str = "Could not find", **kwargs):
        if not await model.objects.get_or_none(**kwargs):
            raise HTTPException(404, detail)

        await model.objects.delete(**kwargs)
