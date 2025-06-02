import os
import time
from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from core.config import settings
from database.init_db import get_db
from models import user
from services.auth import admin_required
from schemas.user import UserUpdate

router = APIRouter()

@router.get("/user")
def get_user(
    offset: Optional[int] = 0,
    limit: Optional[int] = 10,
    return_count: Optional[bool] = False,
    db = Depends(get_db),
    current_user = Depends(admin_required),
):
    users = db.query(user.User).offset(offset).limit(limit).all()

    if return_count:
        resp_objs = len(users)

    else:
        resp_objs = [
            {
                "id": item.id,
                "username": item.username,
                "email": item.email,
                "role": item.role,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for item in users
        ]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy dữ liệu thành công",
            "payload": {
                "users": resp_objs
            }
        }
    )


@router.put("/user")
def update_user(
    update_data: UserUpdate,
    db = Depends(get_db),
    current_user = Depends(admin_required)
):
    existed_user = db.query(user.User).filter(user.User.id == update_data.id).first()

    if not existed_user:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Người dùng không tồn tại",
            }
        )
    
    if update_data.username:
        existed_user.username = update_data.username

    if update_data.password:
        existed_user.password = update_data.password
    
    if update_data.role:
        existed_user.role = update_data.role
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Cập nhật người dùng thành công",
            "payload": {
                "user": {
                    "id": existed_user.id,
                    "username": existed_user.username,
                    "email": existed_user.email,
                    "role": existed_user.role,
                    "created_at": existed_user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
            }
        }
    )