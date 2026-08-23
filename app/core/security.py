import bcrypt
import jwt
from app.core.config import settings
from datetime import datetime, timezone, timedelta

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

# Băm mật khẩu bằng bcrypt trước khi lưu vào cơ sở dữ liệu.
def hash_password(password: str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()

# So sánh mật khẩu người dùng nhập với chuỗi bcrypt đã lưu.
def verify_password(plain_password: str, hash_password: str):
    password = plain_password.encode()
    hashed_password = hash_password.encode()
    return bcrypt.checkpw(password, hashed_password)

# Tạo JWT có thời điểm hết hạn và các thông tin định danh cần thiết.
def create_access_token(data: dict, expires_minutes: int):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return token

# Giải mã JWT; chuyển lỗi thư viện thành ValueError dễ xử lý hơn ở tầng gọi.
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("The token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")