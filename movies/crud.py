"""
Contain movie and rating related CRUD ORM queries/functions to interact with the data in the database.
"""

import uuid
from datetime import datetime

from sqlalchemy import update, delete
from sqlalchemy.orm import Session

from movies import models, schemas


def get_movie_by_id(db: Session, movie_id: str):
    """
    Return movie object with the given ID

    :param db: DB Session object
    :param movie_id: Movie UUID
    :return: DB query object
    """
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movies(db: Session):
    """
    Return list of movies

    :param db: DB Session object
    :return List of movie objects
    """
    return db.query(models.Movie).all()


def get_movies_by_user(db: Session, user_id: str):
    """
    Return list of movies added by a specific user

    :param db: DB Session object
    :param user_id: User UUID
    :return: List of movie objects
    """
    return db.query(models.Movie).filter(models.Movie.added_by == user_id).all()


def add_user(db: Session, movie: schemas.MovieAddRequest, added_by_id: str):
    """
    Create a movie object in the DB

    :param db: DB Session object
    :param movie: Pydantic movie instance
    :param added_by_id: User ID who is trying to add the movie
    :return: DB user object
    """

    db_movie = models.Movie(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        name=movie.name,
        year=movie.year,
        description=movie.description,
        avg_rating=0.0,
        extra=movie.extra,
        added_by=added_by_id
    )

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


def update_movie(db: Session, movie: models.Movie, updated_data: dict):
    """
    Update movie details as part of the partial update

    :param db: DB session object
    :param movie: Current movie object
    :param updated_data: Dict containing updated values
    :return: Refreshed DB object, With update data
    """

    db.execute(update(models.Movie).where(models.Movie.id == movie.id).values(updated_data))

    db.commit()
    db.refresh(movie)

    return movie


def delete_user(db: Session, movie: models.Movie):
    """
    Delete a given movie object from DB

    :param db: DB session object
    :param movie: Current movie object
    :return: None
    """

    db.execute(delete(models.Movie).where(models.Movie.id == movie.id))
    db.commit()
