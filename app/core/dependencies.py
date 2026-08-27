from collections.abc import Generator
import jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.db.database import SessionLocal
from app.models.user import User

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=401,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user_id = int(user_id)
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception
    statement = select(User).where(User.id == user_id)
    user = db.scalar(statement)
    if user is None:
        raise credentials_exception
    return user