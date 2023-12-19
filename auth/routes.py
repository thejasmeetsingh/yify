"""
Contain all user and auth related routes
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

import config
import strings
from auth import crud
from auth.schemas import UserCreate, UserJWT, JWT, UserLogin
from base.utils import get_auth_token, validate_password
from database import get_db

router = APIRouter()


@router.post(path="/register/", response_model=UserJWT, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handler for creating a user object in DB when user signup/register themselves

    :param user: Pydantic UserCreate instance
    :param db: DB session object
    :return: Pydantic user model instance
    """

    try:
        # Check if user already exists
        db_user = crud.get_user_by_email(db=db, email=user.email)
        if db_user:
            raise HTTPException(
                detail=strings.EMAIL_ALREADY_EXISTS,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Create user
        db_user = crud.create_user(db=db, user=user)

        # Generate auth tokens
        jwt_payload = {"user_id": str(db_user.id)}

        access_token = get_auth_token(data=jwt_payload, exp=timedelta(minutes=int(config.ACCESS_TOKEN_EXP_MINUTES)))
        refresh_token = get_auth_token(data=jwt_payload, exp=timedelta(minutes=int(config.REFRESH_TOKEN_EXP_MINUTES)))

        jwt = JWT(access=access_token, refresh=refresh_token)

        return UserJWT(message=strings.ACCOUNT_CREATED_SUCCESS, data=db_user, tokens=jwt)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post(path="/login/", response_model=UserJWT, status_code=status.HTTP_200_OK)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Login API handler

    :param user: Pydantic UserCreate instance
    :param db: DB session object
    :return: Pydantic user model instance
    """

    try:
        # Check if user exists by the given email
        db_user = crud.get_user_by_email(db=db, email=user.email)
        if not db_user:
            raise HTTPException(
                detail=strings.USER_DOES_NOT_EXISTS,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Check user password
        if not validate_password(raw_password=user.password, hashed_password=db_user.password):
            raise HTTPException(
                detail=strings.INVALID_PASSWORD,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Generate auth tokens
        jwt_payload = {"user_id": str(db_user.id)}

        access_token = get_auth_token(data=jwt_payload, exp=timedelta(minutes=int(config.ACCESS_TOKEN_EXP_MINUTES)))
        refresh_token = get_auth_token(data=jwt_payload, exp=timedelta(minutes=int(config.REFRESH_TOKEN_EXP_MINUTES)))

        jwt = JWT(access=access_token, refresh=refresh_token)

        return UserJWT(message=strings.LOGIN_SUCCESS, data=db_user, tokens=jwt)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
