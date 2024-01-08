"""Added request model

Revision ID: 9d268f11872f
Revises: 5bf4eca324f0
Create Date: 2024-01-08 05:05:04.683009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9d268f11872f'
down_revision: Union[str, None] = '5bf4eca324f0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "requests",
        sa.Column("id", sa.UUID, primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime),
        sa.Column("modified_at", sa.DateTime),

        sa.Column("user_id", sa.UUID, sa.ForeignKey(
            "users.id"), nullable=False, index=True),
        sa.Column("name", sa.String(50), unique=True, nullable=False),
    )

    op.create_unique_constraint(
        "unique_movie_request_name",
        "requests",
        ["name"]
    )


def downgrade() -> None:
    op.drop_constraint("unique_movie_request_name", "requests", type_="unique")
    op.drop_table("requests")
