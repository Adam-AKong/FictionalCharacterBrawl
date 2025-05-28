"""add unique constraint for battle_votes between user_id and battle_id

Revision ID: dffe5230606d
Revises: 6cdb5f2e41d5
Create Date: 2025-05-27 21:57:26.730837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dffe5230606d'
down_revision: Union[str, None] = '6cdb5f2e41d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(
    "uix_user_battle_vote",
    "battle_votes",
    ["user_id", "battle_id"]
)



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "uix_user_battle_vote",
        "battle_votes",
        type_="unique"
    )
