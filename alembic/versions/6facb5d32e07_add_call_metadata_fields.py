"""add call metadata fields

Revision ID: 6facb5d32e07
Revises: 86e5447fa030
Create Date: 2026-08-04 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6facb5d32e07'
down_revision: Union[str, Sequence[str], None] = '86e5447fa030'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'calls',
        sa.Column('sentiment', sa.String(length=50), nullable=True),
    )
    op.add_column(
        'calls',
        sa.Column('intent', sa.String(length=50), nullable=True),
    )
    op.add_column(
        'calls',
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.alter_column('calls', 'created_at', server_default=None)


def downgrade() -> None:
    op.drop_column('calls', 'created_at')
    op.drop_column('calls', 'intent')
    op.drop_column('calls', 'sentiment')
