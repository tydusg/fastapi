"""Add foreign key to posts table

Revision ID: 3f4ba2e6c82a
Revises: b29c8bdd99a3
Create Date: 2022-02-24 12:02:33.101921

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f4ba2e6c82a'
down_revision = 'b29c8bdd99a3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE'
                          )


def downgrade():
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
