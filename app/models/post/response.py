from typing import Optional

import ormar
from pydantic import BaseModel


class PostResponse(BaseModel):
    id: Optional[int]
    content: Optional[str]
    date: Optional[ormar.Date]
    time: Optional[ormar.Time]
