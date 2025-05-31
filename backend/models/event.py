from sqlalchemy import Column, Integer, DateTime, String, Enum
from sqlalchemy.orm import relationship

from models.base import Base, BareBaseModel

class Event(BareBaseModel):
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    location = Column(String, nullable=True)
