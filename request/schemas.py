"""
Contain movie request models, Pydantic schemas
"""

from datetime import datetime

from pydantic import BaseModel, UUID4

from auth.schemas import UserPublic


class Request(BaseModel):
    """
    Request base schema
    """

    id: UUID4
    created_at: datetime
    modified_at: datetime
    name: str

    class Config:
        """
        This would tell pydantic to use read the data as an ORM model
        """
        from_attributes = True


class RequestData(BaseModel):
    """
    Request payload schema
    """

    name: str


class RequestUser(BaseModel):
    """
    Request response schema
    """

    id: UUID4
    name: str
    created_at: datetime
    user: UserPublic


class MessageResponse(BaseModel):
    """
    Message response schema
    """

    message: str


class RequestDataResponse(BaseModel):
    """
    Message with data response schema
    """

    message: str
    data: RequestUser


class RequestList(BaseModel):
    """
    Request list schema
    """

    id: UUID4
    name: str
    created_at: datetime


class RequestListResponse(BaseModel):
    """
    Request list response schema
    """

    results: list[RequestList]
