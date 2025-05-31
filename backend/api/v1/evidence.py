import os
import time
from typing import *
from datetime import datetime

from fastapi import APIRouter, Depends, status, UploadFile, File, Form
from fastapi.responses import JSONResponse

from core.config import settings
from database.init_db import get_db
from models import criteria, subcriteria, user_subcriteria, evidence_subcriteria
from services.auth import get_current_user, teacher_required
from schemas.evidence import EvidencePost, EvidenceUpdate

router = APIRouter()

@router.post("/evidence")
def submit_evidence(
    evidence_data: EvidencePost,
    file: UploadFile = File(None),
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Submit evidence for a subcriteria."""
    try:
        # Check if the subcriteria exists
        os.makedirs(os.path.join(settings.STATIC_DIR, "evidence", str(evidence_data.semester), current_user.id), exist_ok=True)
        filename = f"{current_user.id}_{evidence_data.subcriteria_id}_{int(time.time())}{os.path.splitext(file.filename)[1]}"
        file_path = os.path.join(settings.STATIC_DIR, "evidence", str(evidence_data.semester), current_user.id, filename)

        evidence = evidence_subcriteria.Evidence_SubCriteria.create(
            db=db,
            user_id=current_user.id,
            subcriteria_id=evidence_data.subcriteria_id,
            description=evidence_data.description,
            file_path=file_path
        )
        if file:
            with open(file_path, "wb") as f:
                f.write(file.file.read())

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "success": True,
                "message": "Evidence submitted successfully",
                "payload": {
                    "evidence_id": evidence.id,
                    "file_path": evidence.file_path
                }
            }
        )
    
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": str(e)}
        )


@router.put("/evidence")
def update_evidence(
    evidence_data: EvidenceUpdate,
    file: UploadFile = File(None),
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update evidence for a subcriteria."""
    try:
        evidence = evidence_subcriteria.Evidence_SubCriteria.update(
            db=db,
            evidence_update=evidence_data
        )

        if not evidence:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "message": "Evidence not found or you do not have permission to update it"}
            )
        
        if file:
            with open(evidence.file_path, "wb") as f:
                f.write(file.file.read())

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Evidence updated successfully",
                "payload": {
                    "evidence_id": evidence.id,
                    "file_path": evidence.file_path
                }
            }
        )
    
    except Exception as e:
        print(e)
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": str(e)}
        )


@router.put("/evidence/verify")
def verify_evidence(
    evidence_id: int,
    status: Literal["approved", "rejected"] = Form(...),
    db = Depends(get_db),
    current_user = Depends(teacher_required)   
):
    """Verify evidence for a subcriteria."""
    try:
        evidence = db.query(evidence_subcriteria.Evidence_SubCriteria).filter(
            evidence_subcriteria.Evidence_SubCriteria.id == evidence_id,
        ).first()

        if not evidence:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"success": False, "message": "Evidence not found or you do not have permission to verify it"}
            )

        evidence.status = status
        db.commit()
        db.refresh(evidence)

        # Update user_subcriteria status based on evidence verification
        if status == "approved":
            user_subcriteria = db.query(user_subcriteria.User_SubCriteria).filter(
                user_subcriteria.User_SubCriteria.user_id == evidence.user_id,
                user_subcriteria.User_SubCriteria.subcriteria_id == evidence.subcriteria_id,
                user_subcriteria.User_SubCriteria.semester == evidence.semester
            ).first()

            if user_subcriteria:
                if user_subcriteria.self_score is None:
                    user_subcriteria.self_score = 0
                    
                user_subcriteria.self_score += 1
                db.commit()
                db.refresh(user_subcriteria)
                
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Evidence verified successfully",
                "payload": {
                    "evidence_id": evidence.id,
                    "status": evidence.status
                }
            }
        )

    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": str(e)}
        )