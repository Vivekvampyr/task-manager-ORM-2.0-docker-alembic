from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.database import engine
from app.api import tasks,auth
from app.core.limiter import limiter

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,allow_methods=["*"],
    allow_headers=["*"])

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(tasks.router,prefix="/api")
app.include_router(auth.router,prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Task Manager API"}

@app.get("/db_test")
def testdb():
    with engine.connect() as connection:
        result = connection.execute(text("select 01"))
        return {"result": result.scalar()}