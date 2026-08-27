import re
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import UserRegisterRequest, UserLoginRequest
from app.core.security import(
    hash_password, 
    verify_password,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)

# Tìm người dùng theo email để dùng chung cho đăng ký và đăng nhập.
def get_user(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()

# Kiểm tra email trùng, băm password và lưu tài khoản mới.
def register_service(user: UserRegisterRequest, db: Session):
    user_db = get_user(user.email, db)
    if user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
        
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )

    if not re.search(r'\d', user.password): # \d đại diện cho các số 0-9
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain digits"
        )

    # Kiểm tra phải chứa ít nhất 1 ký tự đặc biệt
    if not re.search(r'[@#$%!^&*()_\-+=|<>/,]', user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must contain special characters"
        )
        
    hashed_password = hash_password(user.password)
    new_user = User(
        full_name = user.username,
        email = user.email,
        password_hash = hashed_password,
        role = user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Xác thực thông tin đăng nhập và phát hành JWT cho người dùng hợp lệ.
def login_service(user: UserLoginRequest, db: Session):
    user_db = get_user(user.email, db)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login"
        )

    if not user_db.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is inactive"
        )
    
    if not verify_password(user.password, user_db.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid login"
        )
    
    return {
        "access_token": create_access_token(
            {
                "email": user_db.email,
                "role": user_db.role
            },
            expires_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
        )
    }