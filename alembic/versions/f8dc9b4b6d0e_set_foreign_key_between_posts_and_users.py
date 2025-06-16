"""set foreign key between posts and users

Revision ID: f8dc9b4b6d0e
Revises: 771a776b919e
Create Date: 2025-06-13 16:09:07.708870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f8dc9b4b6d0e'
down_revision: Union[str, None] = '771a776b919e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("posts_users_fk",source_table="posts",referent_table="users",
                          local_cols=['owner_id'],remote_cols=['id'],ondelete=CASCADE)
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
