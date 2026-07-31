"""update notification enum

Revision ID: 3ffa6e516e78
Revises: fd55f611f27e
Create Date: 2026-07-03 07:32:24.889688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3ffa6e516e78"
down_revision: Union[str, Sequence[str], None] = "fd55f611f27e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute(
        "ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'BOARD_CREATED';"
    )

    op.execute(
        "ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'BOARD_UPDATED';"
    )

    op.execute(
        "ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'BOARD_DELETED';"
    )

    op.execute(
        "ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'COMMENT_UPDATED';"
    )

    op.execute(
        "ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'COMMENT_DELETED';"
    )

    op.execute(
        "ALTER TYPE notificationtype ADD VALUE IF NOT EXISTS 'ATTACHMENT_DELETED';"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass