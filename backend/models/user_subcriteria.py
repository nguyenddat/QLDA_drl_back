from sqlalchemy import Column, Integer, DateTime, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.base import Base, BareBaseModel
from models.user import User
from models.subcriteria import SubCriteria

class User_SubCriteria(BareBaseModel):
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    subcriteria_id = Column(Integer, ForeignKey("subcriteria.id"), nullable=False)
    semester = Column(Integer, nullable=False)

    self_score = Column(Integer, nullable=False)
    class_leader_score = Column(Integer, nullable=True)
    teacher_score = Column(Integer, nullable=True)
    
    review_by = Column(Enum("self", "class_leader", "teacher", name="review_by"), default="self")
    last_score = Column(Integer, nullable=True)


    user = relationship("User", back_populates="user_subcriteria")
    subcriteria = relationship("SubCriteria", back_populates="user_subcriteria")