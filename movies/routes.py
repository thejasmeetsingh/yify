"""
Contain all movie and rating related API routes
"""
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
        movie = crud.add_movie_db(
            db=db,
            movie=movie_request,
            added_by_id=str(user.id)
        )

        return schemas.MovieResponse(message=strings.MOVIE_ADDED_SUCCESSFULLY, data=movie)
    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=str(e),
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e

# @router.get(
#     path="/movie/", 
#     response_model=LimitOffsetPage[schemas.MovieListResponse], 
#     status_code=status.HTTP_200_OK
# )
# async def get_movie_list(
#     user: Annotated[User, Depends(get_current_user)],
#     db: Annotated[Session, Depends(get_db)]
# ):
#     pass
