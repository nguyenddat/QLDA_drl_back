from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from database.init_db import get_db
from models import criteria, subcriteria, user_subcriteria
from services.auth import get_current_user
from schemas.criteria import CriteriaUpdate

router = APIRouter()

@router.get("/criteria")
def get_criteria(
    semester: int,
    db=Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    """
    Get all criteria with subcriteria and user scores, optimized to reduce DB queries.
    """
    resp_objs = {}

    # Lấy toàn bộ user_subcriteria của người dùng trong học kỳ này
    user_scores = db.query(user_subcriteria.User_SubCriteria).filter(
        user_subcriteria.User_SubCriteria.user_id == current_user.id,
        user_subcriteria.User_SubCriteria.semester == semester
    ).all()

    # Map theo subcriteria_id cho dễ truy cập
    user_score_map = {
        item.subcriteria_id: item for item in user_scores
    }

    # Lấy toàn bộ criteria và subcriteria trong một lần
    criterias = db.query(criteria.Criteria).all()
    sub_criterias = db.query(subcriteria.SubCriteria).all()

    # Gom subcriteria theo criteria_id
    subcriteria_by_criteria = {}
    for sub in sub_criterias:
        subcriteria_by_criteria.setdefault(sub.parent_criteria_id, []).append(sub)

    for c in criterias:
        resp_objs[c.id] = {
            "id": c.id,
            "name": c.name,
            "min_score": c.min_score,
            "max_score": c.max_score,
            "subcriteria": {}
        }

        for sub in subcriteria_by_criteria.get(c.id, []):
            score = user_score_map.get(sub.id)

            resp_objs[c.id]["subcriteria"][sub.id] = {
                "id": sub.id,
                "name": getattr(sub, "name", None),
                "min_score": sub.min_score,
                "max_score": sub.max_score,
                "self_score": score.self_score if score else None,
                "class_leader_score": getattr(score, "class_leader_score", None) if score else None,
                "teacher_score": getattr(score, "teacher_score", None) if score else None,
            }

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Lấy tiêu chí thành công",
            "payload": {
                "criteria": resp_objs
            }
        }
    )

@router.put("/criteria")
def update_criteria(
    criteria_data: CriteriaUpdate,
    db=Depends(get_db),
    current_user: Any = Depends(get_current_user)
):
    existed = db.query(user_subcriteria.User_SubCriteria).filter(
        user_subcriteria.User_SubCriteria.id == criteria_data.id,
        user_subcriteria.User_SubCriteria.user_id == current_user.id,
        user_subcriteria.User_SubCriteria.semester == criteria_data.semester
    )

    existed = existed.first()
    if not existed:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "message": "Không tìm thấy tiêu chí",
                "payload": {}
            }
        )
    
    existed.self_score = criteria_data.score
    if current_user.role == "student":
        existed.review_by = "self"
    else:
        existed.review_by = current_user.role
    
    existed.last_score = criteria_data.score
    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Cập nhật tiêu chí thành công",
            "payload": {
                "criteria_id": existed.id,
                "score": existed.self_score
            }
        }
    )