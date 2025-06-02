from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from database.init_db import get_db
from services.auth import get_current_user
from ai.recommend.recommend import recommend

router = APIRouter()

@router.get("/recommend")
def get_recommend(
    db=Depends(get_db),
    current_user=Depends(get_current_user)
):
    resp_objs = recommend(db, current_user.id)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy dữ liệu thành công",
            "payload": {
                "recommendations": resp_objs
            }
        }
    )