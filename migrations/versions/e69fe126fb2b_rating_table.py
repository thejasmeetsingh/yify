"""rating table

Revision ID: e69fe126fb2b
Revises: 333c774db1be
Create Date: 2024-01-05 07:58:59.994368

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e69fe126fb2b'
down_revision: Union[str, None] = '333c774db1be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ratings",
        sa.Column("id", sa.UUID, primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("modified_at", sa.DateTime),

        sa.Column("user_id", sa.UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("movie_id", sa.UUID, sa.ForeignKey("movies.id"), nullable=False),
        sa.Column("rating", sa.Float(precision=2, asdecimal=True, decimal_return_scale=2), nullable=False),
        sa.Column("review", sa.String(length=250), nullable=True),
    )

    op.create_unique_constraint(
        "unique_movie_rating",
        "ratings",
        ["user_id", "movie_id"]
    )


def downgrade() -> None:
    op.drop_constraint("unique_movie_rating", "ratings", type_="unique")
    op.drop_table("ratings")
