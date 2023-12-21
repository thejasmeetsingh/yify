from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

import strings
from auth import models, crud
from base.utils import get_jwt_payload
from database import SessionLocal


async def get_db():
    """
    A common function for getting a database session
    :return None
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    """
    A common function for getting user object from the token passed into the headers

    :param request: request object
    :param db: DB session object
    :return: DB user instance
    """

    authorization = request.headers.get('authorization')

    if not authorization or "Bearer" not in authorization:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=strings.AUTH_ERROR)

    _, access_token = authorization.split()

    payload = get_jwt_payload(access_token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=strings.AUTH_ERROR)

    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=strings.AUTH_ERROR)

    db_user = crud.get_user_by_id(db=db, user_id=user_id)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=strings.AUTH_ERROR)

    return db_user
