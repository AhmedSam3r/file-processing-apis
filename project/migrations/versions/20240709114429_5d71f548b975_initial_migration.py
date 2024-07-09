"""Initial migration

Revision ID: 5d71f548b975
Revises: 124a0f779f70
Create Date: 2024-07-09 11:44:29.259772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d71f548b975'
down_revision = '124a0f779f70'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.add_column(sa.Column('alias', sa.Text()))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('file', schema=None) as batch_op:
        batch_op.drop_column('alias')

    # ### end Alembic commands ###