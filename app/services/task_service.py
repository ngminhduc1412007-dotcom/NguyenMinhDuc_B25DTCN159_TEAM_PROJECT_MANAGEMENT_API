from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from app.models.task import Task
from app.models.user import User
from app.models.project import Project, ProjectMember
from app.schemas.task import TaskCreate, TaskUpdate

def create_task_service(id: int, task: TaskCreate, current_user: dict, db: Session):
    # Kiểm tra project được truyền qua URL có tồn tại.
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Tìm user từ thông tin trong token đăng nhập.
    user = db.query(User).filter(User.email == current_user['email']).first()
    if not user:
        # Token còn hợp lệ nhưng tài khoản đã không còn trong database.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )

    # Chỉ cho phép thành viên của project tạo task.
    is_project_member = db.query(ProjectMember).filter(ProjectMember.project_id == id, ProjectMember.user_id == user.id).first()
    if not is_project_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project"
        )
    
    # Owner được giao việc cho member khác; member chỉ được tự nhận task.
    if project.owner_id != user.id and task.assignee_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Members can only assign tasks to themselves"
        )

    # Kiểm tra người được giao task cũng thuộc project này.
    assignee = db.query(User).join(ProjectMember).filter(
        User.id == task.assignee_id,
        ProjectMember.project_id == id,
        ProjectMember.user_id == User.id
    ).first()
    if not assignee:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Assignee is not a member of this project"
            )

    # Lấy dữ liệu từ request và dùng project_id trong URL làm nguồn chính.
    task_data = task.model_dump()
    task_data["project_id"] = id
    new_task = Task(**task_data)

    # Lưu task vào database và hoàn tác nếu xảy ra lỗi.
    try:
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
    except Exception:
        db.rollback()
        raise
    return new_task

def get_tasks_service(
    id: int, current_user: dict, db: Session, search: Optional[str] = None,
    sort_by: str = "created_at", sort_order: str = "asc"
    ):
    project = db.query(Project).filter(Project.id == id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Tìm user từ thông tin trong token đăng nhập.
    user = db.query(User).filter(User.email == current_user['email']).first()
    if not user:
        # Token còn hợp lệ nhưng tài khoản đã không còn trong database.
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )

    # Chỉ cho phép thành viên của project xem task.
    is_project_member = db.query(ProjectMember).filter(ProjectMember.project_id == id, ProjectMember.user_id == user.id).first()
    if not is_project_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project"
        )
        
    if sort_by not in {"created_at", "due_date"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="sort_by must be created_at or due_date"
        )
    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="sort_order must be asc or desc"
        )

    # Chỉ lấy task của project hiện tại rồi mới áp dụng search và phân trang.
    query = db.query(Task).filter(Task.project_id == id)
    search = (search or "").strip()
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    # Chọn cột sắp xếp trong danh sách cho phép, tránh nhận tên cột tùy ý từ client.
    sort_column = Task.created_at if sort_by == "created_at" else Task.due_date
    sort_column = sort_column.asc() if sort_order == "asc" else sort_column.desc()
    # Luôn lấy 5 task đầu tiên sau khi lọc và sắp xếp.
    tasks = query.order_by(sort_column).offset(0).limit(5).all()
    return tasks


def get_task_by_id_service(id: int, current_user: dict, db: Session):
    task = db.query(Task).filter(Task.id == id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    user = db.query(User).filter(User.email == current_user["email"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists"
        )
        
    # Chỉ cho phép thành viên của project xem task.
    is_project_member = db.query(ProjectMember).filter(ProjectMember.project_id == task.project_id, ProjectMember.user_id == user.id).first()
    if not is_project_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not a member of this project"
        )
    return task


def update_task_service(id: int, task_update: TaskUpdate, current_user: dict, db: Session):
    # Lấy task và kiểm tra user thuộc project trước khi cho phép cập nhật.
    task = get_task_by_id_service(id, current_user, db)

    # Tìm user hiện tại và project chứa task để xác định quyền.
    user = db.query(User).filter(User.email == current_user["email"]).first()
    project = db.query(Project).filter(Project.id == task.project_id).first()

    # Owner hoặc assignee của task mới được phép cập nhật.
    is_owner = project.owner_id == user.id
    is_assignee = task.assignee_id == user.id
    if not is_owner and not is_assignee:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner or task assignee can update this task"
        )

    # exclude_unset=True: chỉ lấy các trường client thực sự gửi lên, không ghi đè trường còn lại.
    # Nếu chỉ cần cập nhật 1 trường thì chỉ cần thay đổi trường đó và các trường khác sẽ giữ nguyên
    changes = task_update.model_dump(exclude_unset=True)

    # # Bỏ qua chuỗi rỗng để không ghi đè dữ liệu hiện tại của task.
    # changes = {
    #     key: value for key, value in changes.items()
    #     if not isinstance(value, str) or value.strip()
    # }

    # Assignee không được chuyển task sang cho người khác.
    if "assignee_id" in changes and not is_owner:
        if changes["assignee_id"] != task.assignee_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only the project owner can change the assignee"
            )

    # Nếu thay đổi assignee thì assignee mới phải thuộc cùng project.
    if "assignee_id" in changes:
        assignee = db.query(ProjectMember).filter(ProjectMember.project_id == task.project_id, ProjectMember.user_id == changes["assignee_id"]).first()
        if not assignee:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Assignee is not a member of this project"
            )

    # Cập nhật các trường hợp lệ vào task.
    for key, value in changes.items():
        setattr(task, key, value)

    # Lưu thay đổi và lấy lại dữ liệu mới nhất từ database.
    db.commit()
    db.refresh(task)
    return task


def delete_task_service(id: int, current_user: dict, db: Session):
    # Lấy task và kiểm tra user thuộc project.
    task = get_task_by_id_service(id, current_user, db)

    # Tìm user hiện tại và project chứa task.
    user = db.query(User).filter(User.email == current_user["email"]).first()
    project = db.query(Project).filter(Project.id == task.project_id).first()

    # Chỉ owner của project mới được xóa task.
    if project.owner_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the project owner can delete this task"
        )
    # Lưu thông tin phản hồi trước khi xóa bản ghi.
    deleted_task = {
        "id": task.id,
        "project_id": task.project_id,
        "title": task.title
    }
    # Xóa task và xác nhận transaction.
    db.delete(task)
    db.commit()
    return deleted_task