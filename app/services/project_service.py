from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.project import Project, ProjectMember
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectUpdate

# Tạo project mới và thêm người tạo làm owner.
def create_project_service(project: ProjectCreate, current_user: dict, db: Session):
    if not project.name.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project name must not be empty"
        )

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
    
# Tìm các project mà người dùng hiện tại là thành viên.
def search_project_service(current_user: dict, db: Session, search: Optional[str] = None):
    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )
    search = search.strip().lower()
    # Chỉ tìm trong các project mà user hiện tại là thành viên.
    query = db.query(Project).join(ProjectMember).filter(ProjectMember.user_id == user.id)
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

# Lấy thông tin project nếu người dùng là thành viên.
def get_project_by_id_service(id: int, current_user: dict, db: Session):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )

    is_member = db.query(ProjectMember).filter(ProjectMember.project_id == id, ProjectMember.user_id == user.id).first()
    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project"
        )
    return project

# Cập nhật thông tin project khi người dùng là owner.
def update_project_service(id: int, update_project: ProjectUpdate, current_user: dict, db: Session):
    if not update_project.name.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Project name must not be empty"
        )

    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )
        
    if project.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access rights"
        )
        
    for key, value in update_project.model_dump().items():
        setattr(project, key, value)
    db.commit()
    db.refresh(project)
    return project

# Xóa project khi người dùng là owner.
def delete_project_service(id: int, current_user: dict, db: Session):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )
        
    if project.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No access rights"
        )
    db.delete(project)
    db.commit()
