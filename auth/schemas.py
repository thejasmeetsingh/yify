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
    first_name: str
    last_name: str

    class Config:
        """
        This would tell pydantic to use read the data as an ORM model
        """
        from_attributes = True


class UserCreateRequest(BaseModel):
    """
    User creation request schema
    """

    email: str
    password: str
    first_name: str
    last_name: str


class UserUpdateRequest(BaseModel):
    """
    User update request schema
    """

    email: str = None
    first_name: str = None
    last_name: str = None


class UserLoginRequest(BaseModel):
    """
    User login request schema
    """

    email: str
    password: str


class UserResponse(BaseModel):
    """
    Base user response schema
    """

    message: str
    data: User


class UserMessageResponse(BaseModel):
    """
    User response schema just for returning a message
    """

    message: str


class ChangePasswordRequest(BaseModel):
    """
    Change password request schema
    """

    old_password: str
    new_password: str


class ResetPasswordRequest(BaseModel):
    """
    Reset password request schema
    """

    email: str


class JWTResponse(BaseModel):
    """
    JWT response schema
    """

    access: str
    refresh: str


class UserJWTResponse(UserResponse):
    """
    Response schema for user data with JWT
    """

    tokens: JWTResponse


class RefreshTokenRequest(BaseModel):
    """
    Refresh token request schema
    """

    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """
    Refresh token response schema
    """

    message: str
    data: JWTResponse
