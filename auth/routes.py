"""
Contain all user and auth related routes
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import strings
from auth import crud
from auth.schemas import User, UserCreate
from database import get_db


router = APIRouter()


@router.post("/register/", status_code=status.HTTP_201_CREATED, response_model=User)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Handler for creating a user object in DB when user signup/register themselves

    :param user: Pydantic UserCreate instance
    :param db: DB session object
    :return: Pydantic user model instance
    """

    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_ALREADY_EXISTS
        )
    return crud.create_user(db=db, user=user)
