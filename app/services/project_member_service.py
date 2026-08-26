from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.project import Project, ProjectMember
from app.models.user import User
from app.schemas.project import ProjectMemberCreate
from app.services.project_service import get_project_by_id_service

# Thêm một user vào project khi người dùng là owner.
def add_project_member_service(id: int, member: ProjectMemberCreate, current_user: dict, db: Session):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    owner = db.query(User).filter(User.email == current_user["email"]).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )
    if project.owner_id != owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can manage members"
        )

    user = db.query(User).filter(User.id == member.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot add an inactive user to the project"
        )
    existing_member = db.query(ProjectMember).filter(ProjectMember.project_id == id, ProjectMember.user_id == user.id).first()
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already a member of this project"
        )

    project_member = ProjectMember(
        project_id=id,
        user_id=user.id,
        role=member.role
    )
    db.add(project_member)
    db.commit()
    db.refresh(project_member)
    return project_member

# Xóa member khỏi project nhưng không cho xóa owner.
def remove_project_member_service(id: int, user_id: int, current_user: dict, db: Session):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    owner = db.query(User).filter(User.email == current_user["email"]).first()
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )
    if project.owner_id != owner.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can manage members"
        )

    project_member = db.query(ProjectMember).filter(ProjectMember.project_id == id, ProjectMember.user_id == user_id).first()
    if not project_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project member not found"
        )
    if project_member.role == "owner" or user_id == project.owner_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The project owner cannot be removed"
        )

    db.delete(project_member)
    db.commit()
    return project_member

# Lấy danh sách member và role của một project.
def get_project_members_service(id: int, current_user: dict, db: Session):
    project = get_project_by_id_service(id, current_user, db)
    return db.query(ProjectMember).filter(ProjectMember.project_id == project.id).order_by(ProjectMember.user_id).all()