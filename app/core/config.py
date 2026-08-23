from pydantic_settings import BaseSettings

# Đọc cấu hình ứng dụng từ biến môi trường hoặc file .env.
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        # Cho phép môi trường phát triển lấy giá trị từ file .env.
        env_file = ".env"

    # Tạo một đối tượng cấu hình dùng chung trong toàn bộ ứng dụng.
settings = Settings()