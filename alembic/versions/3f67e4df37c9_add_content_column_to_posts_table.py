"""add content column to posts table

Revision ID: 3f67e4df37c9
Revises: 108e0432cce3
Create Date: 2026-05-28 14:23:49.635621

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f67e4df37c9'
down_revision: Union[str, Sequence[str], None] = '108e0432cce3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','content')
    pass
