"""
Contain user model related pydantic schema
"""

import uuid
from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: uuid.uuid4
    created_at: datetime
    modified_at: datetime
    email: str
    password: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
