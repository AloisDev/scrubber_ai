import logging
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database.db import get_db
from database.users import (
    create_user_in_db,
    decode_token,
    get_all_users,
    get_user_by_email,
    get_user_by_id,
    replace_user_in_db,
    update_user_in_db,
)
from database.db import engine

import models
import schemas

router = APIRouter()

models.Base.metadata.create_all(bind=engine)


@router.post(
    "/users", response_model=schemas.User, tags=["Users"], summary="Create a new user."
)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        logging.error(f"User already registered")
        raise HTTPException(status_code=409, detail="User already registered")
    new_user = create_user_in_db(db=db, user=user)
    logging.info(f"New user with email {new_user.email} created.")
    return new_user


@router.get(
    "/users",
    response_model=list[schemas.User],
    tags=["Users"],
    summary="Get all users.",
)
async def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    users: schemas.User = Depends(decode_token),
):
    users = get_all_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Users"],
    summary="Get a user by id.",
)
async def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    db_user: schemas.User = Depends(decode_token),
):
    db_user = get_user_by_id(db, user_id=user_id)
    if db_user is None:
        logging.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.patch(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Users"],
    summary="Update user by id.",
)
async def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserUpdate = Depends(decode_token),
):
    return update_user_in_db(db=db, user_id=user_id, user=user)


@router.put(
    "/users/{user_id}",
    response_model=schemas.User,
    tags=["Users"],
    summary="Replace a user by id.",
)
async def replace_user(
    user_id: int,
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserUpdate = Depends(decode_token),
):
    return replace_user_in_db(db=db, user_id=user_id, user=user)


@router.delete(
    "/users/{user_id}",
    response_model=None,
    tags=["Users"],
    summary="Delete a user by id.",
)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(decode_token),
):
    current_user = get_user_by_id(db, user_id=user_id)
    if current_user is None:
        logging.error(f"User not found")
        raise HTTPException(status_code=404, detail="User not found")
    username = current_user.first_name + " " + current_user.last_name
    db.delete(current_user)
    db.commit()
    return f"{username} deleted succesfuly"
