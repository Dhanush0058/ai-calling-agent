"""add embedding_id to calls

Revision ID: a2c93b8a9c18
Revises: 6facb5d32e07
Create Date: 2026-08-05 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2c93b8a9c18'
down_revision: Union[str, Sequence[str], None] = '6facb5d32e07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'calls',
        sa.Column('embedding_id', sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    op.drop_column('calls', 'embedding_id')
