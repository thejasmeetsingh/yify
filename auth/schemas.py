"""
Contain user model related pydantic schema
"""

from datetime import datetime

from pydantic import BaseModel, UUID4


class User(BaseModel):
    """
    Base user schema
    """

    id: UUID4
    created_at: datetime
    modified_at: datetime
    email: str
    password: str
    first_name: str
    last_name: str

    class Config:
        """
        This would tell pydantic to use read the data as an ORM model
        """
        from_attributes = True


class UserCreate(BaseModel):
    """
    User creation schema
    """

    email: str
    password: str
    first_name: str
    last_name: str


class UserResponse(BaseModel):
    """
    Base user response schema
    """

    message: str
    data: User


class JWT(BaseModel):
    """
    JWT response schema
    """

    access: str
    refresh: str


class UserJWT(UserResponse):
    """
    Response schema for user data with JWT
    """

    tokens: JWT
