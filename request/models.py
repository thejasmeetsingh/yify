"""
Contains movie request related model
"""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Request(Base):
    """
    Request model, For storing movie request details,
    So that other users can view the request and add the wanted movie
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    # Request raised by
    user_id = sa.Column(sa.UUID, sa.ForeignKey("users.id"), index=True)
    user = relationship("User", back_populates="request")

    # Movie name
    name = sa.Column(sa.String, unique=True, index=True)

    __tablename__ = "requests"

    __table_args__ = (
        sa.UniqueConstraint("name", name="unique_movie_request_name"),
    )

    def __str__(self):
        return self.name
