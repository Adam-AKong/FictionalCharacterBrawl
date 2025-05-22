"""Removed Votes so we can aggregate from votes table

Revision ID: 3582818504a3
Revises: c2a3bc0e7799
Create Date: 2025-05-21 18:11:57.732955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3582818504a3'
down_revision: Union[str, None] = 'c2a3bc0e7799'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('battle', 'vote1')
    op.drop_column('battle', 'vote2')
    op.add_column('battle_votes', sa.Column('char_id', sa.Integer(), nullable=False))
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


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
    """
    DROP VIEW IF EXISTS battle_with_votes;
    """
    )
    op.add_column('battle', sa.Column('vote1', sa.Integer(), nullable=False, server_default=sa.text('0')))
    op.add_column('battle', sa.Column('vote2', sa.Integer(), nullable=False, server_default=sa.text('0')))
    op.drop_column('battle_votes', 'char_id')

