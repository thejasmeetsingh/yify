"""initial

Revision ID: d40cc4e9ceb6
Revises: 
Create Date: 2023-12-08 08:01:23.553012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd40cc4e9ceb6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Users table migration
    """

    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), primary_key=True, index=True),
        sa.Column("created_at", sa.DateTime()),
        sa.Column("modified_at", sa.DateTime()),
        sa.Column("email", sa.String(50), unique=True),
        sa.Column("password", sa.String(255)),
        sa.Column("first_name", sa.String(10)),
        sa.Column("last_name", sa.String(10)),
    )

    op.create_check_constraint(
        "email_validation",
        "users",
        sa.text("email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'")
    )


def downgrade() -> None:
    """
    Users table de-migration
    """

    op.drop_constraint("email_validation", "users", type_="check")
    op.drop_table("users")
