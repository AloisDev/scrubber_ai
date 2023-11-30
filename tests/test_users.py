from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

from models.models import Base, User


from ..config import SQLALCHEMY_DATABASE_URL

from ..schemas import UserCreate


from ..main import app

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_users():
    db = TestingSessionLocal()
    test_user = UserCreate(email="test@example.com", password="test")
    db_user = User(email=test_user.email)
    db_user.hashed_password = pwd_context.hash(test_user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [{"email": "test@example.com"}]
