"""
Contain all movie and rating related API routes
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy import exc
from sqlalchemy.orm import Session

import strings
from auth.models import User
from base.dependencies import get_current_user, get_db
from movies import crud
from movies import schemas

router = APIRouter()


@router.post(
    path="/movie/",
    response_model=schemas.MovieResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_movie(
    movie_request: schemas.MovieAddRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API route for adding a movie

    :param movie_request: Movie request pydantic model instance
    :param user: Current User object
    :param db: DB session object
    :return: Instance of movie schema
    """

    try:
        # Validate movie year
        if not (
            movie_request.year and
            isinstance(movie_request.year, int) and
            1000 <= movie_request.year <= 9999
        ):
            raise HTTPException(detail=strings.INVALID_YEAR_ERROR,
                                status_code=status.HTTP_400_BAD_REQUEST)

        db_movie = crud.add_movie_db(
            db=db,
            movie=movie_request,
            added_by_id=str(user.id)
        )
        setattr(db_movie, "avg_rating", db_movie.get_avg_rating())

        return schemas.MovieResponse(message=strings.MOVIE_ADDED_SUCCESSFULLY, data=db_movie)
    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.get(
    path="/movie/",
    response_model=schemas.MovieListResponse,
    status_code=status.HTTP_200_OK
)
async def get_movie_list(
    limit: int,
    offset: int,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API for getting list of movies

    :param limit: query param
    :param offset: query param
    :param db: DB session object
    :return: Instance of movie list response pydantic model
    """

    db_movies = crud.get_movies_db(db, limit, offset)

    movies = [schemas.MovieList(
        id=db_movie.id,
        name=db_movie.name,
        year=db_movie.year,
        avg_rating=db_movie.get_avg_rating()
    ) for db_movie in db_movies]

    return schemas.MovieListResponse(results=movies)


@router.get(
    path="/movie/{movie_id}/",
    response_model=schemas.MovieResponse,
    status_code=status.HTTP_200_OK
)
async def get_movie_by_id(
    movie_id: uuid.UUID,
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API for getting detail of a movie by its ID

    :param movie_id: Path parameter
    :param db: DB session object
    :return: Instance of movie response pydantic model
    """

    try:
        db_movie = crud.get_movie_by_id_db(db, movie_id)
        setattr(db_movie, "avg_rating", db_movie.get_avg_rating())
        return schemas.MovieResponse(message="", data=db_movie)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=strings.MOVIE_DETAIL_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.patch(
    path="/movie/{movie_id}/",
    response_model=schemas.MovieResponse,
    status_code=status.HTTP_200_OK
)
async def update_movie_detail(
    movie_id: uuid.UUID,
    movie_request: schemas.MovieUpdateRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API route for update a movie details

    :param movie_id: Path parameter
    :param movie_request: Movie update request pydantic model instance
    :param user: Current User object
    :param db: DB session object
    :return: Instance of movie schema
    """

    try:
        db_movie = crud.get_movie_by_id_db(db, movie_id)

        # Check if current is the owener of the given movie
        if db_movie.added_by_id != user.id:
            raise HTTPException(detail=strings.PERMISSION_ERROR,
                                status_code=status.HTTP_403_FORBIDDEN)

        # Validate movie year, if passed
        if movie_request.year and not (
            isinstance(movie_request.year, int) and
            1000 <= movie_request.year <= 9999
        ):
            raise HTTPException(detail=strings.INVALID_YEAR_ERROR,
                                status_code=status.HTTP_400_BAD_REQUEST)

        updated_data = movie_request.model_dump(exclude_unset=True)
        # Check if the passed data is empty
        if not updated_data:
            raise HTTPException(
                detail=strings.INVALID_DATA_PASSED,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        db_movie = crud.update_movie_db(db, db_movie, updated_data)
        setattr(db_movie, "avg_rating", db_movie.get_avg_rating())

        return schemas.MovieResponse(message=strings.MOVIE_UPDATE_SUCCESS, data=db_movie)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=strings.MOVIE_UPDATE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.delete(
    path="/movie/{movie_id}/",
    response_model=schemas.GenericMessageResponse,
    status_code=status.HTTP_200_OK
)
async def delete_movie(
    movie_id: uuid.UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API route to delete a movie

    :param movie_id: Path parameter
    :param user: Current User object
    :param db: DB session object
    :return: Instance of generic message response schema
    """

    try:
        db_movie = crud.get_movie_by_id_db(db, movie_id)

        # Check if current is the owener of the given movie
        if db_movie.added_by_id != user.id:
            raise HTTPException(detail=strings.PERMISSION_ERROR,
                                status_code=status.HTTP_403_FORBIDDEN)

        crud.delete_movie_db(db, db_movie)
        return schemas.GenericMessageResponse(message=strings.MOVIE_DELETE_SUCCESS)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=strings.MOVIE_DELETE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.get(
    path="/user-movie/",
    response_model=schemas.MovieListResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_movie_list(
    limit: int,
    offset: int,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API for getting list of movies added by a user

    :param limit: query param
    :param offset: query param
    :param user: Current User object
    :param db: DB session object
    :return: Instance of movie list response pydantic model
    """

    db_movies = crud.get_movies_by_user_db(db, user.id, limit, offset)

    movies = [schemas.MovieList(
        id=db_movie.id,
        name=db_movie.name,
        year=db_movie.year,
        avg_rating=db_movie.get_avg_rating()
    ) for db_movie in db_movies]

    return schemas.MovieListResponse(results=movies)


@router.post(
    path="/rating/",
    response_model=schemas.RatingResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_rating(
    rating_request: schemas.RatingRequest,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """
    API adding rating & review of a movie

    :param rating_request: Rating request
    :param user: Current User object
    :param db: DB session object
    :return: Instance of rating response schema
    """

    try:
        if not (
            0 <= rating_request.rating <= 10
        ):
            raise HTTPException(
                detail=strings.RATING_VALUE_ERROR,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        db_rating = crud.add_rating_db(db, rating_request, user.id)
        rating = schemas.Rating(rating=db_rating.rating, review=db_rating.review)

        return schemas.RatingResponse(message=strings.ADD_RATING_SUCCESS, data=rating)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=strings.ADD_RATING_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e
