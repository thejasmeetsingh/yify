"""
Contain user profile related model
"""

import peewee

from base.models import BaseModel


class User(BaseModel):
    """
    A user with basic fields which represent as a user profile
    """

    email = peewee.CharField(
        max_length=50, 
        unique=True, 
        index=True, 
        constraints=[peewee.CharField.check('email ~ \'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$\'')]
    )
    password = peewee.CharField(max_length=50)
    first_name = peewee.CharField(max_length=20)
    last_name = peewee.CharField(max_length=20)

    class Meta:
        table_name = "user"