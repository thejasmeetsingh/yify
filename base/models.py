"""
Contain base model which will inherited by all models in the application
"""

import uuid
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from database import Base


class BaseModel(Base):
    """
    Contain common fields which will be used by every model
    """

    id: Mapped[uuid.uuid4] = mapped_column(
        primary_key=True,
        index=True,
        default=uuid.uuid4()
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
    modified_at: Mapped[datetime] = mapped_column(default=datetime.utcnow())
