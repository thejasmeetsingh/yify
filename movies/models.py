"""
Contain movie related model
"""

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from database import Base


class Movie(Base):
    """
    Movie model, For storing movie details which is added by a user
    :note Movie name will be unique throughout the application
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    added_by = sa.Column(sa.UUID, sa.ForeignKey("users.id"), index=True)
    name = sa.Column(sa.String, unique=True, index=True)
    year = sa.Column(sa.Integer)
    description = sa.Column(sa.Text(length=2000), nullable=True)
    avg_rating = sa.Column(sa.Float(precision=2, asdecimal=True, decimal_return_scale=2))
    extra = sa.Column(sa.JSON, default={})  # This will store any other metadata related to the movie

    user = relationship("User", back_populates="users")

    __tablename__ = "movies"

    __table_args__ = (
        sa.UniqueConstraint("name", name="unique_movie_name"),
    )

    def __str__(self):
        return self.name


class Rating(Base):
    """
    Store rating given by user to a movie
    """

    id = sa.Column(sa.UUID, primary_key=True, index=True)
    created_at = sa.Column(sa.DateTime)
    modified_at = sa.Column(sa.DateTime)

    user_id = sa.Column(sa.UUID, sa.ForeignKey("users.id"))
    movie_id = sa.Column(sa.UUID, sa.ForeignKey("movies.id"))
    rating = sa.Column(sa.Float(precision=2, asdecimal=True, decimal_return_scale=2))
    review = sa.Column(sa.String, nullable=True)

    __tablename__ = "ratings"

    __table_args__ = (
        sa.UniqueConstraint("user_id", "movie_id", name="unique_movie_rating"),
    )

    def __str__(self):
        return self.created_at
