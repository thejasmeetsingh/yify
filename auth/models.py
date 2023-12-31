"""
Contain user profile related model
"""

import re

import sqlalchemy as sa
from sqlalchemy.orm import validates, relationship

from database import Base

import strings


class User(Base):
    """
    A user with basic fields which represent as a user profile
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    email = sa.Column(sa.String, unique=True, index=True)
    password = sa.Column(sa.String)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)

    rating = relationship("Rating", back_populates="user")
    request = relationship("Request", back_populates="user")

    __tablename__ = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @validates("email_validation")
    def validate_email(self, _, value):
        """
        RegEx for email validation
        """

        if not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
            raise ValueError(strings.INVALID_EMAIL)
        return value
