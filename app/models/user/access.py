from typing import Dict, Optional, Union

import ormar

from setup import BaseMeta

from .profile import ProfileModel

# user - editor - admin


class AccessModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "access"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    user: Optional[Union[ProfileModel, Dict]] = ormar.ForeignKey(
        ProfileModel,
        related_name="access",
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    access = ormar.String(max_length=15, default="user")
