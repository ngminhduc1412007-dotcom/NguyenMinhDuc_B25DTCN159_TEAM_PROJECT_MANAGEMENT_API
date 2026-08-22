from fastapi import FastAPI, HTTPException
from app.db.database import engine, Base
from app.core.exceptions import register_exception_handlers
from app.routers.auth import routers as auth_router
from app.routers.admin import routers as admin_router
from app.routers.users import routers as user_router
from app.models import project, task, user

app = FastAPI()

Base.metadata.create_all(bind=engine)

register_exception_handlers(app)

@app.get("/health-check")
def checking_server():
    raise HTTPException(
        status_code=200,
        detail="Server is running"
    )
    
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(user_router)