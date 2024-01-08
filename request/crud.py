"""
Contain request model related CRUD ORM queries/functions 
"""

import uuid
from datetime import datetime

from sqlalchemy import delete
from sqlalchemy.orm import Session

from movies.models import Movie
from request import models, schemas


def add_request_db(db: Session, request: schemas.RequestData, user_id: uuid.UUID):
    """
    Add request object to DB

    :param db: DB Session object
    :param request: Request schema instance
    :param user_id: Movie UUID
    """

    db_request = models.Request(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        user_id=user_id,
        name=request.name,
    )

    db.add(db_request)
    db.commit()

    return db_request


def get_request_detail_db(db: Session, request_id: uuid.UUID):
    """
    Get details of a request object by ID from DB

    :param db: DB Session object
    :param request_id: Request UUID
    """

    return db.query(models.Request).get(request_id)


def delete_request_db(db: Session, request_id: uuid.UUID):
    """
    Delete request object from DB

    :param db: DB Session object
    :param request_id: Request UUID
    """

    db.execute(delete(models.Request).where(models.Request.id == request_id))
    db.commit()


def get_movie_by_name_db(db: Session, name: str):
    """
    Get boolean depicting a movie object exists or not, This will ensure no request
    gets created for those movies which are already added

    :param db: DB Session object
    :param name: movie name
    """

    return db.query(Movie).filter_by(name=name).first()


def get_request_list_db(db: Session, search: str, limit: int, offset: int):
    """
    Get request list from DB

    :param db: DB Session object
    :param search: search based on movie name
    :param limit: Limit the resulting rows
    :param offset: Offset for the rows
    """

    return db.query(models.Request).filter(
        models.Request.name.like(f"%{search}%")
    ).limit(limit).offset(offset).all()


def get_requests_by_user_db(db: Session, user_id: uuid.UUID, limit: int, offset: int):
    """
    Get requests raised by given user

    :param db: DB Session object
    :param user_id: User UUID
    :param limit: Limit the resulting rows
    :param offset: Offset for the rows
    """

    return db.query(models.Request).filter_by(user_id=user_id).limit(limit).offset(offset).all()
