from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.core.security import hash_password

router = APIRouter(prefix="/auth",tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.scalar(statement)
    if existing_user is not None:
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(email=user_data.email,password_hash=hash_password(user_data.password),first_name=user_data.first_name,last_name=user_data.last_name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user