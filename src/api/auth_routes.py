from db import *
import twitter
from fastapi import FastAPI, Request
from models import *
from typing import List
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from datetime import datetime, timedelta
from typing import Union
from limiter import limiter
from fastapi import APIRouter
from auth_helpers import *

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365


@router.post("/token/", response_model=Token)
@limiter.limit("5/minute")
async def login_for_access_token(
    request: Request, form_data: OAuth2PasswordRequestForm = Depends()
):
    with Session(engine) as session:
        user = authenticate_user(session, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


class RegisterInfo(BaseModel):
    username: str
    password: str
    twitter_username: str = ""


@router.post("/api/register/")
async def register(info: RegisterInfo):
    raise HTTPException(
        status_code=400,
        detail="Registrations are currently closed.",
    )
    with Session(engine) as session:
        user = get_user(session, username=info.username)
        if not user:
            if len(info.password) < 11:
                raise HTTPException(
                    status_code=400,
                    detail="Password length minimum 12 characters. Plain words are fine",
                )
            ph = get_password_hash(password=info.password)
            try:
                twitter_uid = twitter.get_user_id(info.twitter_username)
                if not twitter_uid:
                    raise HTTPException(
                        status_code=400,
                        detail="Failed to get twitter user id",
                    )
            except:
                raise HTTPException(
                    status_code=400,
                    detail="Failed to get twitter user id",
                )
            user = User(
                username=info.username,
                hashed_password=ph,
                role="user",
                twitter_uid=str(twitter_uid),
                twitter_username=info.twitter_username,
            )
            session.add(user)
            session.commit()
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user.username}, expires_delta=access_token_expires
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
            }
        else:
            raise HTTPException(
                status_code=400,
                detail="Username already taken",
            )


@router.get("/api/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
