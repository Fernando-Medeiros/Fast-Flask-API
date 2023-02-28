from datetime import datetime
from typing import Dict, Optional, Union

import ormar

from setup import BaseMeta

from ..user import ProfileModel


class PostModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "posts"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    author: Optional[Union[ProfileModel, Dict]] = ormar.ForeignKey(
        ProfileModel,
        related_name="posts",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    content = ormar.Text(nullable=False)
    edit = ormar.Boolean(default=False)
    created_at = ormar.DateTime(default=datetime.today, nullable=False)
