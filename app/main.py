from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.db.database import engine, Base
from app.core.exceptions import http_exception_handler

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_exception_handler(
    HTTPException,
    http_exception_handler
)

@app.get("/check/server")
def checking_server():
    raise HTTPException(
        status_code=200,
        detail="Server is running"
    )

@app.get("/test/400")
def test_400():
    raise HTTPException(
        status_code=400,
        detail="Invalid request"
    )