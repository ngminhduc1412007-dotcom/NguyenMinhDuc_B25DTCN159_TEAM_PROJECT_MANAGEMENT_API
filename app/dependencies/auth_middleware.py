from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from app.core.security import decode_access_token

security = HTTPBearer()

def get_current_user(cred: HTTPAuthorizationCredentials = Depends(security)):
    token = cred.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid token"
        )
    return payload

def get_current_admin(current_user = Depends(get_current_user)):
    if current_user['role'] != "admin":
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "No access rights"
        )
    return current_user