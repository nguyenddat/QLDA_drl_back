from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import user_subcriteria, evidence_subcriteria
from services.auth import teacher_required

router = APIRouter()

@router.get("/dashboard/criteria")
def get_dashboard_criteria(
    review_by: str,
    return_count: Optional[bool] = False,
    semester: Optional[int] = None,
    db=Depends(get_db),
    current_user=Depends(teacher_required)
):
    sub_criterias = db.query(user_subcriteria.User_SubCriteria).filter(
        user_subcriteria.User_SubCriteria.review_by == review_by
    )

    if semester is not None:
        sub_criterias = sub_criterias.filter(
            user_subcriteria.User_SubCriteria.semester == semester
        )
    
    sub_criterias = sub_criterias.all()
    if return_count:
        resp_objs = len(sub_criterias)
    
    else:
        resp_objs = [{"id": item.id,
                    "subcriteria_id": item.subcriteria_id,
                    "semester": item.semester,
                    "self_score": item.self_score,
                    "class_leader_score": item.class_leader_score,
                    "teacher_score": item.teacher_score,
                    "review_by": item.review_by,
                    "last_score": item.last_score}
                    for item in sub_criterias] 

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy dữ liệu thành công",
            "payload": {
                "criteria": resp_objs
            }
        }
    )

@router.get("/dashboard/evidence")
def get_dashboard_evidence(
    status: str,
    return_count: Optional[bool] = False,
    semester: Optional[int] = None,
    db = Depends(get_db),
    current_user=Depends(teacher_required)
):
    evidences = db.query(evidence_subcriteria.Evidence_SubCriteria).filter(
        evidence_subcriteria.Evidence_SubCriteria.status == status
    )

    if semester is not None:
        evidences = evidences.filter(
            evidence_subcriteria.Evidence_SubCriteria.semester == semester
        )
    
    evidences = evidences.all()
    if return_count:
        resp_objs = len(evidences)
    else:
        resp_objs = [{"id": item.id,
                    "user_id": item.user_id,
                    "subcriteria_id": item.subcriteria_id,
                    "semester": item.semester,
                    "description": item.description,
                    "file_path": item.file_path,
                    "status": item.status}
                    for item in evidences]
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy dữ liệu thành công",
            "payload": {
                "evidence": resp_objs
            }
        }
    )