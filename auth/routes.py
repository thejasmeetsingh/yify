"""
Contain all user and auth related routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

import strings
from auth import crud
from auth.models import User
from auth.schemas import UserCreate, UserJWT, JWT, UserLogin, RefreshToken, RefreshTokenResponse, UserResponse
from base.utils import validate_password, generate_auth_tokens, get_jwt_payload
from base.dependencies import get_db, get_current_user

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
        auth_tokens = generate_auth_tokens(db_user)
        jwt = JWT(access=auth_tokens["access"], refresh=auth_tokens["refresh"])

        return UserJWT(message=strings.ACCOUNT_CREATED_SUCCESS, data=db_user, tokens=jwt)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


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
        auth_tokens = generate_auth_tokens(db_user)
        jwt = JWT(access=auth_tokens["access"], refresh=auth_tokens["refresh"])

        return UserJWT(message=strings.LOGIN_SUCCESS, data=db_user, tokens=jwt)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.post(path="/refresh-token/", response_model=RefreshTokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(token: RefreshToken, db: Session = Depends(get_db)):
    """
    API handler for refreshing access token

    :param token: Refresh token instance
    :param db: DB session object
    :return: Pydantic JWT model instance
    """

    # Perform validations checks on the token
    if not token.refresh_token:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    payload = get_jwt_payload(token.refresh_token)

    if not payload:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    db_user = crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(
            detail=strings.INVALID_TOKEN,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    # Generate auth tokens
    auth_tokens = generate_auth_tokens(db_user)
    jwt = JWT(access=auth_tokens["access"], refresh=auth_tokens["refresh"])

    return RefreshTokenResponse(message=strings.TOKEN_REFRESH_SUCCESS, data=jwt)


@router.get(path="/profile/", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def profile_details(user: User = Depends(get_current_user)):
    """
    API for fetching current user profile details

    :param user: User object
    :return: Instance of user response schema
    """

    return UserResponse(message=strings.PROFILE_DETAILS_SUCCESS, data=user)
