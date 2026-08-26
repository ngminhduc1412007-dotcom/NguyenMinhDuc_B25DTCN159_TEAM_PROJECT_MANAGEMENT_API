from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import decode_access_token
from app.db.database import get_db
from app.models.user import User

# HTTPBearer đọc token từ header Authorization dạng Bearer.
security = HTTPBearer()

# Xác thực token và trả về payload của người dùng hiện tại.
def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = cred.credentials
    try:
        payload = decode_access_token(token)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    email = payload.get("email")
    user = db.query(User).filter(User.email == email).first() if email else None
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive or no longer exists",
        )

    return {
        **payload,
        "email": user.email,
        "role": user.role,
    }

# Giới hạn endpoint chỉ cho payload có role admin truy cập.
def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No access rights",
        )
    return current_user