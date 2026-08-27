from fastapi import APIRouter, HTTPException, Depends, status
from fastapi import Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.core.security import hash_password
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password
from app.core.limiter import limiter

router = APIRouter(prefix="/auth",tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
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

@router.post("/login",response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    statement = select(User).where(User.email == form_data.username)
    user = db.scalar(statement)
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    if not verify_password(form_data.password,user.password_hash):
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token,"token_type": "bearer"}