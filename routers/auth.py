from fastapi import APIRouter, FastAPI
from datetime import timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from database.db import get_db
from database.users import authenticate_user, create_access_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.schemas import Token

router = APIRouter()


# This token endpoint accespts username and password (in form) and returns a token.
# this option has a grant_type, username, password,  client_id and client_secret fields that can be used out of the box as it uses OAuth2PasswordRequestForm


@router.post("/token", response_model=Token, tags=["Auth"], summary="Get access token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": f"Bearer {access_token}"}


# This endpoint accepts a username and password as json and returns a token. All field requeired can be added to the schema as needed.

# @app.router("/token", response_model=schemas.Token,tags=["auth"])
# async def login_for_access_token(
#     form_data: schemas.TokenRequestForm,
#     db: Session = Depends(get_db)
# ):
#     user = crud.authenticate_user(db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = crud.create_access_token(
#         data={"sub": user.email}, expires_delta=access_token_expires
#     )
#     return {"access_token": f'Bearer {access_token}'}
