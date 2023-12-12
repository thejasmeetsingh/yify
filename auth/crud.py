"""
Contain user related CRUD ORM queries/functions to interact with the data in the database.
"""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from auth import models, schemas
from base import utils


def get_user_by_id(db: Session, user_id: str):
    """
    Return user object with the given ID

    :param db: DB Session object
    :param user_id: User UUID
    :return: DB query object
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """
    Return user object with the given ID

    :param db: DB Session object
    :param email: User email address
    :return: DB query object
    """
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create a user object in the DB

    :param db: DB Session object
    :param user: Pydantic user instance
    :return: DB user object
    """
    hashed_password = utils.get_hashed_password(user.password)
    db_user = models.User(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        email=user.email.lower(),
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
