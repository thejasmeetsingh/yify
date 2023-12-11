"""
Contain user related CRUD ORM queries/functions to interact with the data in the database.
"""

import uuid
from datetime import datetime

from sqlalchemy.orm import Session

import models
import schemas
from base import utils


def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id==user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_hashed_password(user.password)
    db_user = models.User(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
