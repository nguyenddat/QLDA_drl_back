from typing import *

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models.user import User
from schemas.auth import UserCreate
from services.auth import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/register")
def register(
    user_data: UserCreate, 
    db: Session = Depends(get_db)
) -> Any:
    
    """Đăng ký người dùng mới"""
    try:
        status_code, user = User.create(db, user_data)
        return JSONResponse(
            status_code=status_code,
            content={
                "success": True, 
                "message": "Đăng ký thành công" if status_code == 201 else "Tên đăng nhập đã tồn tại",
                "payload": {"user": {"username": user.username}} if status_code == 201 else {"user": None}
            }
        )
    except Exception as e:
        print(f"Error during user registration: {e}")
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Đã xảy ra lỗi khi đăng ký người dùng",
                "error": str(e)
            }
        )
    

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """Đăng nhập và lấy token"""
    status_code, user = User.authenticate(db, form_data.username, form_data.password)
    if status_code != 200:
        raise HTTPException(
            status_code=status_code,
            detail="Tên đăng nhập hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id)
    refresh_token = create_refresh_token(subject=user.id)
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Đăng nhập thành công",
            "payload": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }}
        )