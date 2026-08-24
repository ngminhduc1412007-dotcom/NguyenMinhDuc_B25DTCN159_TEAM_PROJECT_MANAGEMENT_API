from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.user_service import security_user_data

# Lấy user theo id, tìm theo từ khóa hoặc trả về toàn bộ user.
def get_users_service(db: Session, search: Optional[str] = None, is_active: Optional[bool] = None):
    query = db.query(User).order_by(User.id)
    if search:
        search = search.strip().lower()
        query = query.filter(
            User.email.ilike(f"%{search}%") | 
            User.full_name.ilike(f"%{search}%")
        )
        
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    users = query.all()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return [security_user_data(user) for user in users]