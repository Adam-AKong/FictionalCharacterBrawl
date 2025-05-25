"""updating battle with votes view

Revision ID: dbdac9b627de
Revises: 3432f6dff460
Create Date: 2025-05-25 15:21:12.819077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dbdac9b627de'
down_revision: Union[str, None] = '3432f6dff460'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
    """
    DROP VIEW IF EXISTS battle_with_votes;
    """
    )
    op.execute(
    """
    CREATE VIEW battle_with_votes AS
    SELECT
        b.id AS id,
        b.user_id AS user_id,
        b.char1_id AS char1_id,
        b.char2_id AS char2_id,
        SUM(CASE WHEN bv.char_id = b.char1_id THEN 1 ELSE 0 END) AS vote1,
        SUM(CASE WHEN bv.char_id = b.char2_id THEN 1 ELSE 0 END) AS vote2,
        b.winner_id AS winner_id,
        b.start_date AS start_date,
        b.end_date AS end_date
        
    FROM
        battle b
    LEFT JOIN
        battle_votes bv ON bv.battle_id = b.id
    GROUP BY
        b.id, b.char1_id, b.char2_id;
    """ 
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
    op.execute(
    """
    DROP VIEW IF EXISTS battle_with_votes;
    """
    )
    op.execute(
    """
    CREATE VIEW battle_with_votes AS
    SELECT
        b.id AS id,
        b.char1_id AS char1_id,
        b.char2_id AS char2_id,
        SUM(CASE WHEN bv.char_id = b.char1_id THEN 1 ELSE 0 END) AS vote1,
        SUM(CASE WHEN bv.char_id = b.char2_id THEN 1 ELSE 0 END) AS vote2,
        b.winner_id AS winner_id,
        b.start_date AS start_date,
        b.end_date AS end_date
        
    FROM
        battle b
    LEFT JOIN
        battle_votes bv ON bv.battle_id = b.id
    GROUP BY
        b.id, b.char1_id, b.char2_id;
    """ 
    )