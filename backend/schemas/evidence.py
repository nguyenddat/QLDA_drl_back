from typing import *

from pydantic import BaseModel, Field

class EvidencePost(BaseModel):
    subcriteria_id: int
    semester: int
    description: str

class EvidenceUpdate(BaseModel):
    id: int
    subcriteria_id: Optional[int] = None
    semester: Optional[int] = None
    description: Optional[str] = None