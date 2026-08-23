from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

# Model công việc thuộc một project và có thể được giao cho một user.
class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(30), nullable=False, default="TODO")
    priority = Column(String(30), nullable=False, default="MEDIUM")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    # Quan hệ ngược tới project chứa task.
    project = relationship(
        "Project",
        back_populates="tasks"
    )

    # Quan hệ ngược tới user được giao task, có thể là None.
    assignee = relationship(
        "User",
        back_populates="assigned_tasks"
    )