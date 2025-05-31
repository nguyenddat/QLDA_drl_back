from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.base import Base, BareBaseModel
from models.user import User
from models.subcriteria import SubCriteria
from schemas.evidence import EvidencePost, EvidenceUpdate

class Evidence_SubCriteria(BareBaseModel):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    subcriteria_id = Column(Integer, ForeignKey("subcriteria.id"), nullable=False)
    semester = Column(Integer, nullable=False)

    description = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(Enum("pending", "approved", "rejected", name="evidence_status"), default="pending")

    user = relationship("User", back_populates="evidence_subcriteria")
    subcriteria = relationship("SubCriteria", back_populates="evidence_subcriteria")

    @staticmethod
    def create(db, user_id: int, subcriteria_id: int, description: str, file_path: str):
        """Create a new evidence entry."""
        evidence = Evidence_SubCriteria(
            user_id=user_id,
            subcriteria_id=subcriteria_id,
            description=description,
            file_path=file_path
        )
        db.add(evidence)
        db.commit()
        db.refresh(evidence)
        return evidence
    
    @staticmethod
    def update(db, evidence_update: EvidenceUpdate):
        """Update an existing evidence entry."""
        evidence = db.query(Evidence_SubCriteria).filter(
            Evidence_SubCriteria.id == evidence_update.id
        ).first()
        
        if not evidence:
            return None
        
        if evidence_update.subcriteria_id is not None:
            evidence.subcriteria_id = evidence_update.subcriteria_id
        if evidence_update.description is not None:
            evidence.description = evidence_update.description
        
        db.commit()
        db.refresh(evidence)
        return evidence
        
