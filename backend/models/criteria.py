from sqlalchemy import Column, Integer, DateTime, String, Enum
from sqlalchemy.orm import relationship

from models.base import Base, BareBaseModel

class Criteria(BareBaseModel):
    name = Column(String, nullable=False)
    
    min_score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)

    subcriteria = relationship("SubCriteria", back_populates="criteria", cascade="all, delete-orphan")