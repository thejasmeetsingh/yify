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
    description: str = None
    extra: dict


class MovieUpdateRequest(BaseModel):
    """
    Movie update request schema
    """

    name: str = None
    year: int = None
    description: str = None
    extra: dict = None


class MovieResponse(BaseModel):
    """
    Movie response schema
    """

    message: str
    data: Movie


class GenericMessageResponse(BaseModel):
    """
    Generic message response schema
    """

    message: str


class RatingRequest(BaseModel):
    """
    Movie rating request schema
    """

    movie_id: UUID4
    rating: float
    review: str = None


class Rating(BaseModel):
    """
    Rating response base schema
    """

    id: UUID4
    rating: float
    review: str | None


class RatingResponse(BaseModel):
    """
    Rating response schema
    """

    message: str
    data: Rating


class RatingListResponse(BaseModel):
    """
    Rating list response schema
    """

    results: list[Rating]


class MovieList(BaseModel):
    """
    Base movie list schema
    """

    id: UUID4
    name: str
    year: int
    avg_rating: float


class MovieListResponse(BaseModel):
    """
    Movie list response schema
    """

    results: list[MovieList]


class RatingMovieList(BaseModel):
    """
    Schema for rating list given by a user to movies
    """

    id: UUID4
    rating: float
    review: str | None
    movie: MovieList


class RatingListMovieResponse(BaseModel):
    """
    Response schema for rating list, Given by a user to movies
    """

    results: list[RatingMovieList]


class UserRating(BaseModel):
    """
    User rating schema
    """

    id: UUID4
    first_name: str
    last_name: str


class RatingUserList(BaseModel):
    """
    Schema for rating list given by users to a movies
    """

    id: UUID4
    rating: float
    review: str | None
    user: UserRating


class RatingUserListResponse(BaseModel):
    """
    Response schema for a movie given by users
    """

    results: list[RatingUserList]
