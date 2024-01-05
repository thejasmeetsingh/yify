"""
Contain movie and rating related CRUD ORM queries/functions to interact with the data in the database.
"""

import uuid
from datetime import datetime

from sqlalchemy import update, delete
from sqlalchemy.orm import Session

from movies import models, schemas


def get_movie_by_id_db(db: Session, movie_id: str):
    """
    Return movie object with the given ID

    :param db: DB Session object
    :param movie_id: Movie UUID
    :return: DB query object
    """
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movies_db(db: Session):
    """
    Return list of movies

    :param db: DB Session object
    :return List of movie objects
    """
    return db.query(models.Movie).all()


def get_movies_by_user_db(db: Session, user_id: str):
    """
    Return list of movies added by a specific user

    :param db: DB Session object
    :param user_id: User UUID
    :return: List of movie objects
    """
    return db.query(models.Movie).filter(models.Movie.added_by == user_id).all()


def add_movie_db(db: Session, movie: schemas.MovieAddRequest, added_by_id: str):
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
        extra=movie.extra,
        added_by=added_by_id
    )

    db.add(db_movie)
    db.commit()

    return db_movie


def update_movie_db(db: Session, movie: models.Movie, updated_data: dict):
    """
    Update movie details as part of the partial update

    :param db: DB session object
    :param movie: Current movie object
    :param updated_data: Dict containing updated values
    :return: Refreshed DB object, With update data
    """

    db.execute(update(models.Movie).where(
        models.Movie.id == movie.id).values(updated_data))

    db.commit()
    db.refresh(movie)

    return movie


def delete_movie_db(db: Session, movie: models.Movie):
    """
    Delete a given movie object from DB

    :param db: DB session object
    :param movie: Current movie object
    :return: None
    """

    db.execute(delete(models.Movie).where(models.Movie.id == movie.id))
    db.commit()


def add_rating_db(db: Session, rating_request: schemas.RatingRequest, user_id: str):
    """
    Add rating of a movie in DB

    :param db: DB session object
    :param rating_request: Pydantic rating instance
    :param user_id: Current User UUID
    """

    db_rating = models.Rating(
        id=uuid.uuid4(),
        created_at=datetime.utcnow(),
        modified_at=datetime.utcnow(),
        user_id=user_id,
        movie_id=rating_request.movie_id,
        rating=rating_request.rating,
        review=rating_request.review
    )

    db.add(db_rating)
    db.commit()

    # Update movie rating stat
    with db.begin():
        movie = db.query(models.Movie).filter_by(
            id=rating_request.movie_id
        ).with_for_update().first()

        movie.ratings_count += 1
        movie.ratings_sum += rating_request.rating

        db.add(movie)
        db.commit()

    return db_rating


def get_movie_ratings_db(db: Session, movie_id: str):
    """
    Get ratings by a specific movie

    :param db: DB session object
    :param movie_id: Movie UUID
    """

    return db.query(models.Rating).filter_by(movie_id=movie_id).all()


def get_user_ratings_db(db: Session, user_id: str):
    """
    Get ratings posted by a user

    :param db: DB session object
    :param user_id: User UUID
    """

    return db.query(models.Rating).filter_by(user_id=user_id).all()
