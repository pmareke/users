"""first_migration

Revision ID: b1bf927741b3
Revises:
Create Date: 2025-06-15 10:18:25.954643

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "b1bf927741b3"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), autoincrement=False, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("age", sa.Numeric(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
