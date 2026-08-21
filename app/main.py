from fastapi import FastAPI, HTTPException
from app.db.database import engine, Base
from app.core.exceptions import register_exception_handlers
from app.routers.auth import routers as auth_router
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

@app.get("/error-test/400")
def test_400():
    raise HTTPException(
        status_code=400,
        detail="Invalid request"
    )
    
app.include_router(auth_router)