"""added rating stat

Revision ID: 5bf4eca324f0
Revises: e69fe126fb2b
Create Date: 2024-01-05 16:48:03.787429

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bf4eca324f0'
down_revision: Union[str, None] = 'e69fe126fb2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("movies", sa.Column("ratings_count", sa.Integer, default=0))
    op.add_column("movies", sa.Column("ratings_sum", sa.Float, default=0.0))
    op.drop_column("movies", "avg_rating")


def downgrade() -> None:
    op.drop_column("movies", "ratings_count")
    op.drop_column("movies", "ratings_sum")
    op.add_column("movies", sa.Column(
        "avg_rating",
        sa.Float(precision=2, asdecimal=True, decimal_return_scale=2)
    ))
