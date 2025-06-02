from typing import *

from pydantic import BaseModel

class CriteriaUpdate(BaseModel):
    id: int
    semester: int
    score: int
