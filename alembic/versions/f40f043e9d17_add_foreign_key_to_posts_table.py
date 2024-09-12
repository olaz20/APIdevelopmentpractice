"""add foreign-key to posts table

Revision ID: f40f043e9d17
Revises: c923c3d5af36
Create Date: 2024-09-11 02:33:01.935589

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f40f043e9d17'
down_revision: Union[str, None] = 'c923c3d5af36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=["owner_id"]
                          , remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() :
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
