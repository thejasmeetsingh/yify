"""movie table

Revision ID: 333c774db1be
Revises: d40cc4e9ceb6
Create Date: 2024-01-05 07:24:32.472641

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '333c774db1be'
down_revision: Union[str, None] = 'd40cc4e9ceb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "movies",
        sa.Column("id", sa.UUID, primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("modified_at", sa.DateTime),

        sa.Column("added_by_id", sa.UUID, sa.ForeignKey("users.id"), nullable=False),
        sa.Column("name", sa.String(50), unique=True, index=True),
        sa.Column("year", sa.Integer),
        sa.Column("description", sa.String(2000), nullable=True),
        sa.Column("avg_rating", sa.Float(precision=2, asdecimal=True, decimal_return_scale=2)),
        sa.Column("extra", sa.JSON, default={}),
    )

    op.create_unique_constraint(
        "unique_movie_name",
        "movies",
        ["name"]
    )


def downgrade() -> None:
    op.drop_constraint("unique_movie_name", "movies", type_="unique")
    op.drop_table("movies")
