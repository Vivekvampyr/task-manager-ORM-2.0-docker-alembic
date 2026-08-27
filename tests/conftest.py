import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.config import settings
from app.core.dependencies import get_db
from app.db.database import Base
from app.models.user import User
from app.core.security import hash_password, create_access_token


TEST_DATABASE_URL = settings.TEST_DATABASE_URL

test_engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=test_engine)

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

        Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    user = User(
        email="test@example.com",
        password_hash=hash_password("testpassword123"),
        first_name="Test",
        last_name="User",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(
        data={"sub": str(test_user.id)}
    )

    return {
        "Authorization": f"Bearer {token}"
    }

@pytest.fixture
def second_user(db):
    user = User(
        email="second@example.com",
        password_hash=hash_password("testpassword123"),
        first_name="Second",
        last_name="User",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

@pytest.fixture
def second_auth_headers(second_user):
    token = create_access_token(
        data={"sub": str(second_user.id)}
    )

    return {
        "Authorization": f"Bearer {token}"
    }