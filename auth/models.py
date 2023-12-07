"""
Contain user profile related model
"""

from sqlalchemy.orm import Mapped, mapped_column

from base.models import BaseModel


class User(BaseModel):
    """
    A user with basic fields which represent as a user profile
    """

    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()

    __tablename__ = "user"