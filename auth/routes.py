"""
Contain all user and auth related routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

import strings
from auth import crud
from auth.schemas import UserCreate, UserResponse
from database import get_db

router = APIRouter()


@router.post(path="/register/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handler for creating a user object in DB when user signup/register themselves

    :param user: Pydantic UserCreate instance
    :param db: DB session object
    :return: Pydantic user model instance
    """

    try:
        db_user = crud.get_user_by_email(db=db, email=user.email)
        if db_user:
            raise HTTPException(
                detail=strings.EMAIL_ALREADY_EXISTS,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        db_user = crud.create_user(db=db, user=user)
        return UserResponse(message=strings.ACCOUNT_CREATED_SUCCESS, data=db_user)
    except exc.SQLAlchemyError as e:
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
