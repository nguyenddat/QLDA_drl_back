from typing import *
from datetime import datetime

from uuid import UUID
from pydantic import BaseModel, Field

from helpers.enum import UserRoleEnum

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    
class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: UserRoleEnum
    avatar: Optional[str] = None
    banner: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class RefreshToken(BaseModel):
    refresh_token: str