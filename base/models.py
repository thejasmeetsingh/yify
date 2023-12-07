"""
Contain base model which will inherited by all models in the application
"""

import uuid
import peewee
from datetime import datetime

from database import DB


class BaseModel(peewee.Model):
    """
    Contain common fields which will be used by every model
    """

    id = peewee.UUIDField(primary_key=True, index=True, default=uuid.uuid4())
    created_at = peewee.DateTimeField(default=datetime.utcnow())
    modified_at = peewee.DateTimeField(default=datetime.utcnow())

    class Meta:
        database = DB
