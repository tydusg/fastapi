"""Add last few columns to posts table

Revision ID: b56648100c63
Revises: 3f4ba2e6c82a
Create Date: 2022-02-24 13:26:57.410076

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b56648100c63'
down_revision = '3f4ba2e6c82a'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='True'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    
def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')