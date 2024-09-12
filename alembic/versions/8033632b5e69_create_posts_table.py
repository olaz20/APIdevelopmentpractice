"""create posts table

Revision ID: 8033632b5e69
Revises: 
Create Date: 2024-09-11 00:57:31.522154

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8033632b5e69'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() :
   op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True,)
    , sa.Column('title',sa.String(), nullable=False))   
   pass


def downgrade():
    op.drop_table('posts')
    pass
