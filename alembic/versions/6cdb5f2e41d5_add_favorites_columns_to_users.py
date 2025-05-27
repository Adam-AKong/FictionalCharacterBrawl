"""add favorites columns to users

Revision ID: 6cdb5f2e41d5
Revises: 9451e3247e5a
Create Date: 2025-05-25 17:00:28.887426

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cdb5f2e41d5'
down_revision: Union[str, None] = '9451e3247e5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('fav_char_id', sa.Integer(), sa.ForeignKey('character.id'), nullable=True))
    op.add_column('user', sa.Column('fav_fran_id', sa.Integer(), sa.ForeignKey('character.id'), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'fav_char_id')
    op.drop_column('user', 'fav_fran_id')
