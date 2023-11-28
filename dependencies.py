import logging
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
    SecurityScopes,
)
from jose import JWTError, jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from constants import ALGORITHM, SECRET_KEY, SQLALCHEMY_DATABASE_URL
import models
import schemas
from dotenv import load_dotenv
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext

engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
auth_scheme = HTTPBearer()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


load_dotenv()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user_in_db(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        logging.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    if user.email is not None:
        db_user.email = user.email
    if user.password is not None:
        db_user.password = get_password_hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user


def replace_user_in_db(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        logging.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    for var, value in user.model_dump().items():
        setattr(db_user, var, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_in_db(db: Session, user: schemas.UserCreate):
    hashedPassword = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        firstName=user.firstName,
        lastName=user.lastName,
        password=hashedPassword,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def decode_token(token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = get_user_by_email(db, username)
    if user is None:
        raise credentials_exception
    return user


async def process_document_in_ai(
    db: Session, document: schemas.Document
) -> schemas.OpenAIResponse:
    response = schemas.OpenAIResponse(
        Determination="Denied",
        Reasoning="Reasoning:\n\n1. The CPT code 3288F is a performance measure code used for reporting purposes only. It is not a reimbursable service, hence it is not covered by insurance.\n\n2. The ICD-10 codes provided, B35.1 (Tinea unguium) and M72.2 (Plantar fascial fibromatosis), do not align with the CPT code 3288F. The CPT code 3288F is used to report the percentage of patients aged 18 years and older with a diagnosis of COPD (Chronic Obstructive Pulmonary Disease) who have an FEV1/FVC less than 70% and have symptoms of dyspnea.\n\n3. The ICD-10 codes B35.1 and M72.2 are related to dermatological and musculoskeletal conditions respectively, not respiratory conditions. Therefore, these diagnoses do not support the use of the CPT code 3288F.\n\n4. The claim lacks the necessary documentation to support the medical necessity of the service provided. The insurance policy requires that the services provided must be medically necessary and appropriate for the diagnosis.\n\n5. The claim does not meet the insurance policy's coverage criteria for the CPT code 3288F. The policy requires that the CPT code and the ICD-10 codes must be compatible and the service provided must be covered under the policy.\n\nDue to these reasons, the claim for CPT code 3288F with ICD-10 codes B35.1 and M72.2 is denied.",
        Query="The Claim for CPT code 3288F with ICD-10 codes: B35.1 M72.2",
        Context="",
        Raw_Output="Determination: Denied\n\nReasoning:\n\n1. The CPT code 3288F is a performance measure code used for reporting purposes only. It is not a reimbursable service, hence it is not covered by insurance.\n\n2. The ICD-10 codes provided, B35.1 (Tinea unguium) and M72.2 (Plantar fascial fibromatosis), do not align with the CPT code 3288F. The CPT code 3288F is used to report the percentage of patients aged 18 years and older with a diagnosis of COPD (Chronic Obstructive Pulmonary Disease) who have an FEV1/FVC less than 70% and have symptoms of dyspnea.\n\n3. The ICD-10 codes B35.1 and M72.2 are related to dermatological and musculoskeletal conditions respectively, not respiratory conditions. Therefore, these diagnoses do not support the use of the CPT code 3288F.\n\n4. The claim lacks the necessary documentation to support the medical necessity of the service provided. The insurance policy requires that the services provided must be medically necessary and appropriate for the diagnosis.\n\n5. The claim does not meet the insurance policy's coverage criteria for the CPT code 3288F. The policy requires that the CPT code and the ICD-10 codes must be compatible and the service provided must be covered under the policy.\n\nDue to these reasons, the claim for CPT code 3288F with ICD-10 codes B35.1 and M72.2 is denied.",
    )
    return response
