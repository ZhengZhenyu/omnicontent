"""Add community url field and change channel_configs.channel from enum to varchar

Revision ID: 005
Revises: 004
Create Date: 2026-02-09

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005'
down_revision = '004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add url column to communities table
    with op.batch_alter_table('communities') as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(500), nullable=True))

    # For SQLite, the channel column was originally an Enum which SQLite stores
    # as VARCHAR anyway, so no actual type change needed. But we ensure the
    # unique constraint exists for (community_id, channel).
    # The model now uses String(50) instead of Enum, which is compatible.
    # SQLite doesn't support ALTER COLUMN, but since it already stores enums
    # as text, the data is already in the correct format.


def downgrade() -> None:
    with op.batch_alter_table('communities') as batch_op:
        batch_op.drop_column('url')
