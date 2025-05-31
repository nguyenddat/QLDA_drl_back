from sqlalchemy import Column, Integer, DateTime, String, Enum
from sqlalchemy.orm import relationship

from models.base import Base, BareBaseModel
from schemas.auth import UserCreate, UserResponse

class User(BareBaseModel):
    name = Column(String)
    username = Column(String, unique=True)
    password = Column(String)

    role = Column(Enum("admin", "student", "class_leader", "teacher", name="user_role"), default = "student")

    user_subcriteria = relationship("User_SubCriteria", back_populates="user", cascade="all, delete-orphan")
    evidence_subcriteria = relationship("Evidence_SubCriteria", back_populates="user", cascade="all, delete-orphan")

    @staticmethod
    def create(db, user_data: UserCreate):
        """Create a new user."""
        existed_user = db.query(User).filter(User.username == user_data.username).first()
        if existed_user:
            return 409, None
        
        else:
            user = User(
                name=None,
                username=user_data.username,
                password=user_data.password,
                role=user_data.role if hasattr(user_data, 'role') else "student"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return 201, user
    
    @staticmethod
    def authenticate(db, username: str, password: str):
        """Authenticate user by username and password."""
        user = db.query(User).filter(User.username == username).first()
        if not user or user.password != password:
            return 401, None
        
        return 200, user