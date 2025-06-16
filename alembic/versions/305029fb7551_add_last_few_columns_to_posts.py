"""add last few columns to posts

Revision ID: 305029fb7551
Revises: f8dc9b4b6d0e
Create Date: 2025-06-13 17:05:57.305999

"""
from typing import Sequence, Union
from wsgiref.simple_server import server_version

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '305029fb7551'
down_revision: Union[str, None] = 'f8dc9b4b6d0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="TRUE"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
