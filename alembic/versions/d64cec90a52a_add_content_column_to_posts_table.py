"""add content column to posts table

Revision ID: d64cec90a52a
Revises: 2218f62f08f1
Create Date: 2022-02-05 14:24:45.117484

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd64cec90a52a'
down_revision = '2218f62f08f1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
