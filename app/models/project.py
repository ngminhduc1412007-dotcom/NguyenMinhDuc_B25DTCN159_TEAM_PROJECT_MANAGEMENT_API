from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

# Model project, liên kết với người sở hữu, thành viên và các task.
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    # Liên kết ngược tới tài khoản sở hữu project.
    owner = relationship(
        "User",
        back_populates="owned_projects"
    )

    # Xóa bản ghi thành viên cùng project khi project bị xóa.
    # delete-orphan (xóa đối tượng mồ côi): Hệ thống tự động quét và 
    # xóa sạch các bản ghi mồ côi này trong cơ sở dữ liệu.
    members = relationship(
        "ProjectMember",
        back_populates="project",
        cascade="all, delete-orphan" 
    )

    # Xóa các task phụ thuộc cùng project khi project bị xóa.
    tasks = relationship(
        "Task",
        back_populates="project",
        cascade="all, delete-orphan"
    )

# Bảng liên kết nhiều-nhiều giữa project và user, kèm role thành viên.
class ProjectMember(Base):
    __tablename__ = "project_members"
    project_id = Column(Integer, ForeignKey("projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(30), nullable=False)
    joined_at = Column(DateTime, default=datetime.now, nullable=False)

    project = relationship(
        "Project",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="project_members"
    )