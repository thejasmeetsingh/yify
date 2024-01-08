"""
Contain movie request related API routes and handlers
"""

import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import exc
from sqlalchemy.orm import Session

import strings
from auth.models import User
from auth.schemas import UserPublic
from request import schemas, crud
from base.dependencies import get_current_user, get_db


router = APIRouter()


@router.post(
    path="/request/",
    response_model=schemas.RequestDataResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_movie_request(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    request_data: schemas.RequestData
):
    """
    API for adding movie request

    :param: user: Current user object
    :param db: DB session object
    :param request: Request model schema instance
    :return: Instance of request response schema 
    """

    try:
        db_movie = crud.get_movie_by_name_db(db, request_data.name)

        if db_movie:
            raise HTTPException(
                detail=strings.REQUEST_MOVIE_ALREADY_EXISTS,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        db_request = crud.add_request_db(db, request_data, user.id)

        request = schemas.RequestUser(
            id=db_request.id,
            name=db_request.name,
            created_at=db_request.created_at,
            user=UserPublic(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name
            )
        )

        return schemas.RequestDataResponse(message=strings.REQUEST_ADD_SUCCESS, data=request)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=strings.REQUEST_ADD_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.get(
    path="/request/{request_id}/",
    response_model=schemas.RequestDataResponse,
    status_code=status.HTTP_200_OK
)
async def get_request_detail(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    request_id: uuid.UUID
):
    """
    API for getting request detail

    :param db: DB session object
    :param request_id: Request UUID
    :return: Instance of request response schema 
    """

    db_request = crud.get_request_detail_db(db, request_id)
    request = schemas.RequestUser(
        id=db_request.id,
        name=db_request.name,
        created_at=db_request.created_at,
        user=UserPublic(
            id=db_request.user.id,
            first_name=db_request.user.first_name,
            last_name=db_request.user.last_name
        )
    )

    return schemas.RequestDataResponse(message="", data=request)


@router.delete(
    path="/request/{request_id}/",
    response_model=schemas.MessageResponse,
    status_code=status.HTTP_200_OK
)
async def delete_request(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    request_id: uuid.UUID
):
    """
    API for deleting request object

    :param db: DB session object
    :param request_id: Request UUID
    :return: Instance of message response schema 
    """

    try:
        db_request = crud.get_request_detail_db(db, request_id)

        if db_request.user_id != user.id:
            raise HTTPException(
                detail=strings.PERMISSION_ERROR,
                status_code=status.HTTP_403_FORBIDDEN
            )

        crud.delete_request_db(db, request_id)
        return schemas.MessageResponse(message=strings.REQUEST_DELETE_SUCCESS)

    except exc.SQLAlchemyError as e:
        # Sent error response if any SQL exception caught
        raise HTTPException(
            detail=strings.REQUEST_DELETE_ERROR,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) from e


@router.get(
    path="/request/",
    response_model=schemas.RequestListResponse,
    status_code=status.HTTP_200_OK
)
async def get_request_list(
    _: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: int,
    offset: int,
    search: str = ""
):
    """
    API for getting list of requests

    :param db: DB session object
    :param limit: query param
    :param offset: query param
    :param search: Search parameter
    :return: Instance of request list response schema
    """

    db_requests = crud.get_request_list_db(db, search, limit, offset)

    requests = [schemas.RequestList(
        id=db_request.id,
        created_at=db_request.created_at,
        name=db_request.name
    ) for db_request in db_requests]

    return schemas.RequestListResponse(results=requests)


@router.get(
    path="/user-request/",
    response_model=schemas.RequestListResponse,
    status_code=status.HTTP_200_OK
)
async def get_user_request_list(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: int,
    offset: int
):
    """
    API for getting list of requests created/raised by current user

    :param user: Current user object
    :param db: DB session object
    :param limit: query param
    :param offset: query param
    :return: Instance of request list response schema
    """

    db_requests = crud.get_requests_by_user_db(db, user.id, limit, offset)

    requests = [schemas.RequestList(
        id=db_request.id,
        created_at=db_request.created_at,
        name=db_request.name
    ) for db_request in db_requests]

    return schemas.RequestListResponse(results=requests)
