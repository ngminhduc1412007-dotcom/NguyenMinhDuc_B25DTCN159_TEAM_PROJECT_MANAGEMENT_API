from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(30), default="user", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    
    owned_projects = relationship(
        "Project",
        back_populates="owner"
    )

    project_members = relationship(
        "ProjectMember",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    assigned_tasks = relationship(
        "Task",
        back_populates="assignee"
    )