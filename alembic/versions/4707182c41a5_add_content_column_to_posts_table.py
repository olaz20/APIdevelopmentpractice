"""add content column to posts table

Revision ID: 4707182c41a5
Revises: 8033632b5e69
Create Date: 2024-09-11 01:43:45.408764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4707182c41a5'
down_revision: Union[str, None] = '8033632b5e69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None




def upgrade() :
     op.add_column('posts', sa.Column('content', sa.String(), nullable=False))                              
     pass

def downgrade() :
    op.drop_table('posts', 'content')
    pass
