"""Create posts table

Revision ID: a0b8f09c194f
Revises: 
Create Date: 2022-02-24 10:51:54.937345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0b8f09c194f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
                    sa.Column('title', sa.String(), nullable=False)
                    )
    


def downgrade():
    op.drop_table('posts')
