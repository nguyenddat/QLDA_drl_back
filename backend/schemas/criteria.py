from typing import *

from pydantic import BaseModel

class CriteriaUpdate(BaseModel):
    id: int
    score: int
    semester: int
    user_id: Optional[int] = None
