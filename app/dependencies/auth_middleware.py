from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.core.security import decode_access_token

# HTTPBearer đọc token từ header Authorization dạng Bearer.
security = HTTPBearer()

# Xác thực token và trả về payload của người dùng hiện tại.
def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    token = cred.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token"
        )
    return payload

# Giới hạn endpoint chỉ cho payload có role admin truy cập.
def get_current_admin(current_user = Depends(get_current_user)):
    if current_user['role'] != "admin":
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "No access rights"
        )
    return current_user