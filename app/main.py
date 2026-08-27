from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.db.database import engine
from app.api import tasks,auth

app = FastAPI(title="Task Manager API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials=True,allow_methods=["*"],
    allow_headers=["*"])

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