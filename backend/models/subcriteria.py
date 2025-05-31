from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.base import Base, BareBaseModel
from models.criteria import Criteria

class SubCriteria(BareBaseModel):
    parent_criteria_id = Column(Integer, ForeignKey("criteria.id"), nullable=False)

    name = Column(String, nullable=False)
    min_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)

    required_evidence = Column(Boolean, default=False)

    criteria = relationship("Criteria", back_populates="subcriteria")
    user_subcriteria = relationship("User_SubCriteria", back_populates="subcriteria", cascade="all, delete-orphan")
    evidence_subcriteria = relationship("Evidence_SubCriteria", back_populates="subcriteria", cascade="all, delete-orphan")