from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Engine quản lý kết nối giữa SQLAlchemy và cơ sở dữ liệu cấu hình trong settings.
engine = create_engine(settings.DATABASE_URL)

# Mỗi request sẽ nhận một session riêng, không tự flush và không hết hạn object sau commit.
SessionLocal = sessionmaker(
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency tạo session cho request và luôn đóng session sau khi request kết thúc.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()