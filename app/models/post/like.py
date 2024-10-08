from typing import Dict, Optional, Union

import ormar

from setup import BaseMeta

from ..user import ProfileModel
from .post import PostModel
from .reply import ReplyModel


class LikeModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "likes"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    user: Optional[Union[ProfileModel, Dict]] = ormar.ForeignKey(
        ProfileModel,
        related_name="likes",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    post: Optional[Union[PostModel, Dict]] = ormar.ForeignKey(
        PostModel,
        related_name="likes",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    reply: Optional[Union[ReplyModel, Dict]] = ormar.ForeignKey(
        ReplyModel,
        related_name="likes",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
