"""first_migration

Revision ID: 2884b90dffc8
Revises:
Create Date: 2025-06-14 18:23:04.597319

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "2884b90dffc8"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String(length=36), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("age", sa.Numeric(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
