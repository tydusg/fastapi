"""Add content column to posts table

Revision ID: f21c74d31a32
Revises: a0b8f09c194f
Create Date: 2022-02-24 11:23:24.563338

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f21c74d31a32'
down_revision = 'a0b8f09c194f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
