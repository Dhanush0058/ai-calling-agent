"""create calls table

Revision ID: 86e5447fa030
Revises: 1694e1913d43
Create Date: 2026-08-02 11:51:48.673926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86e5447fa030'
down_revision: Union[str, Sequence[str], None] = '1694e1913d43'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # This revision is a duplicate history entry; the `calls` table is already
    # created in the prior revision 1694e1913d43.
    pass


def downgrade() -> None:
    """Downgrade schema."""
    # No schema change here because the table is managed by the previous revision.
    pass
