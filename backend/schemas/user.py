from typing import *

from pydantic import BaseModel

class UserUpdate(BaseModel):
    id: int
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None