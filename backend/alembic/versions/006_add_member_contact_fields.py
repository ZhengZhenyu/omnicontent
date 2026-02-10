"""Add contact fields to committee members

Revision ID: 006
Revises: 005
Create Date: 2026-02-10

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Make email and organization NOT NULL
    op.alter_column('committee_members', 'email',
                    existing_type=sa.String(200),
                    nullable=False)
    op.alter_column('committee_members', 'organization',
                    existing_type=sa.String(200),
                    nullable=False)
    
    # Add new optional contact fields
    op.add_column('committee_members', sa.Column('gitcode_id', sa.String(100), nullable=True))
    op.add_column('committee_members', sa.Column('github_id', sa.String(100), nullable=True))


def downgrade() -> None:
    # Remove new fields
    op.drop_column('committee_members', 'github_id')
    op.drop_column('committee_members', 'gitcode_id')
    
    # Revert email and organization to nullable
    op.alter_column('committee_members', 'organization',
                    existing_type=sa.String(200),
                    nullable=True)
    op.alter_column('committee_members', 'email',
                    existing_type=sa.String(200),
                    nullable=True)
