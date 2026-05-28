"""add last few columns to posts table

Revision ID: 0a1bfb2e9c2d
Revises: 4ddcfb76cfd6
Create Date: 2026-05-28 14:47:58.456677

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a1bfb2e9c2d'
down_revision: Union[str, Sequence[str], None] = '4ddcfb76cfd6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts',
            sa.Column('published', sa.Boolean(),nullable=False,server_default='True'))
    op.add_column('posts',
             sa.Column('created_at', sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
