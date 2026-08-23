from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.project import Project, ProjectMember
from app.models.user import User
from app.schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    ProjectMemberCreate, ProjectMemberUpdate, ProjectMemberResponse
)

def create_project_service(project: ProjectCreate, current_user: dict, db: Session):
    # Tìm user đang đăng nhập từ email được lưu trong JWT.
    user = db.query(User).filter(User.email == current_user['email']).first()
    if not user:
        # Token còn hợp lệ nhưng tài khoản đã không còn trong database.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )

    # Tạo project và gán user hiện tại làm chủ sở hữu.
    new_project = Project(
        **project.model_dump(),
        owner_id=user.id
    )

    # Flush để database sinh new_project.id trước khi tạo bản ghi thành viên.
    db.add(new_project)
    db.flush()

    # Lưu user vào bảng liên kết với vai trò chủ project.
    owner_project = ProjectMember(
        project_id=new_project.id,
        user_id=user.id,
        role="owner"
    )

    # Commit project và thành viên owner trong cùng một transaction.
    db.add(owner_project)
    db.commit()
    db.refresh(new_project)
    return new_project
    
def search_project_service(db: Session, search: Optional[str] = None):
    # Chuẩn hóa từ khóa; search=None sẽ trở thành chuỗi rỗng.
    search = search.strip().lower()

    # Tạo query ban đầu, chưa thực thi truy vấn trên database.
    query = db.query(Project)
    if search:
        # Tìm project có tên chứa từ khóa, không phân biệt hoa thường.
        query = query.filter(Project.name.ilike(f"%{search}%"))

    # Sắp xếp theo ID rồi thực thi query để lấy danh sách kết quả.
    projects = query.order_by(Project.id).all()
    if not projects:
        # Không có project phù hợp thì trả lỗi 404 cho client.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No projects found"
        )
    return projects