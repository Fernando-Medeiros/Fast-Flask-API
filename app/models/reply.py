from datetime import datetime
from typing import Dict, Optional, Union

import ormar

from app.services.database import BaseMeta

from .post import PostModel
from .profile import ProfileModel


class ReplyModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "replies"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    author: Optional[Union[ProfileModel, Dict]] = ormar.ForeignKey(
        ProfileModel,
        related_name="replies",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    post: Optional[Union[PostModel, Dict]] = ormar.ForeignKey(
        PostModel,
        related_name="replies",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    content = ormar.Text(nullable=False)
    edit = ormar.Boolean(default=False)
    created_at = ormar.DateTime(default=datetime.today, nullable=False)
