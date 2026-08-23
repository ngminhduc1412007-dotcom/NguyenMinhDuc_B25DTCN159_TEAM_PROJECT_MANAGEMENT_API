from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.user_service import security_user_data

# Lấy toàn bộ user theo id và loại bỏ trường password khỏi kết quả.
def get_all_user_service(db: Session):
    users = db.query(User).order_by(User.id).all()
    return [security_user_data(user) for user in users]

# Tìm user theo id và báo lỗi nếu không tồn tại.
def get_user_by_id_service(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return security_user_data(user)

# Lọc danh sách theo email hoặc họ tên nếu người quản trị truyền từ khóa.
def list_users_service(db: Session, search: Optional[str] = None):
    users = db.query(User).order_by(User.id).all()
    if search:
        search = search.strip().lower()
        users = [user for user in users if search in user.email.lower() or search in user.full_name.lower()]
    return [security_user_data(user) for user in users]