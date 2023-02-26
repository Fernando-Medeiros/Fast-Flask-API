from typing import Dict, Optional, Union

import ormar

from app.services.database import BaseMeta

from .profile import ProfileModel


class BirthdayModel(ormar.Model):
    class Meta(BaseMeta):
        tablename = "birthday"

    id = ormar.Integer(primary_key=True, autoincrement=True)
    user: Optional[Union[ProfileModel, Dict]] = ormar.ForeignKey(
        ProfileModel,
        related_name="birthday",
        unique=True,
        onupdate=ormar.ReferentialAction("CASCADE"),
        ondelete=ormar.ReferentialAction("CASCADE"),
    )
    day = ormar.String(max_length=2, nullable=False)
    month = ormar.String(max_length=2, nullable=False)
    year = ormar.String(min_length=2, max_length=4, nullable=False)
