"""add content to post table

Revision ID: fd596e940a46
Revises: 6a961c7bdae9
Create Date: 2025-06-13 15:30:29.689638

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd596e940a46'
down_revision: Union[str, None] = '6a961c7bdae9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))

    pass


def downgrade() -> None:
    op.drop_column("content")
    """Downgrade schema."""

    pass
