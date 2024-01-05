"""
Contain movie and rating models related pydantic schemas
"""


from datetime import datetime

from pydantic import BaseModel, UUID4


class Movie(BaseModel):
    """
    Base user schema
    """

    id: UUID4
    created_at: datetime
    modified_at: datetime
    name: str
    year: int
    description: str | None
    avg_rating: float
    extra: dict

    class Config:
        """
        This would tell pydantic to use read the data as an ORM model
        """
        from_attributes = True


class MovieAddRequest(BaseModel):
    """
    Movie add request schema
    """

    name: str
    year: int
    description: str | None
    extra: dict


class RatingRequest(BaseModel):
    """
    Movie rating request schema
    """

    movie_id: UUID4
    rating: float
    review: str | None
