from functools import wraps

import ormar


def post(model : ormar.Model):
    def inner (func):

        @wraps(func)
        async def wrap(request_model: ormar.Model):
            attr = request_model.dict(exclude_unset=True)
            user = model(**attr)
            return await user.save()

        return wrap
    return inner

