"""
Contain user related CRUD ORM queries/functions to interact with the data in the database.
"""

import uuid
from datetime import datetime

from sqlalchemy import update, delete
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
    return db.query(models.User).get(user_id)


def get_user_by_email(db: Session, email: str):
    """
    Return user object with the given ID

    :param db: DB Session object
    :param email: User email address
    :return: DB query object
    """
    return db.query(models.User).filter(models.User.email == email.lower()).first()


def create_user(db: Session, user: schemas.UserCreateRequest):
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

    return db_user


def update_user(db: Session, user: models.User, updated_data: dict):
    """
    Update user details as part of the partial update

    :param db: DB session object
    :param user: Current user object
    :param updated_data: Dict containing updated values
    :return: Refreshed DB object, With update data
    """

    db.execute(update(models.User).where(
        models.User.id == user.id).values(updated_data))

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user: models.User):
    """
    Delete a given user object from DB

    :param db: DB session object
    :param user: Current user object
    :return: None
    """

    db.execute(delete(models.User).where(models.User.id == user.id))
    db.commit()
