"""
Contain user profile related model
"""

import re
from sqlalchemy.orm import Mapped, mapped_column, validates

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

    @validates("email_validation")
    def validate_email(self, _, value):
        """
        RegEx for email validation
        """

        if not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError("Invalid email address")
        return value
