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


class UserCreate(BaseModel):
    """
    User creation schema
    """

    email: str
    password: str
    first_name: str
    last_name: str


class UserUpdate(BaseModel):
    """
    User update schema
    """

    email: str = None
    first_name: str = None
    last_name: str = None


class UserLogin(BaseModel):
    """
    User login schema
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


class ChangePassword(BaseModel):
    """
    Change password schema
    """

    old_password: str
    new_password: str


class ResetPassword(BaseModel):
    """
    Reset password schema
    """

    email: str


class ResetPasswordForm(BaseModel):
    """
    Reset password form schema
    """

    password: str
    confirm_password: str
    token: str


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


class RefreshToken(BaseModel):
    """
    Refresh token schema
    """

    refresh_token: str


class RefreshTokenResponse(BaseModel):
    """
    Token response schema
    """

    message: str
    data: JWT
