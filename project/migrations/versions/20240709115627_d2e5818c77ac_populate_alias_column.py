"""populate alias column

Revision ID: d2e5818c77ac
Revises: 5d71f548b975
Create Date: 2024-07-09 11:56:27.487353

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'd2e5818c77ac'
down_revision = '5d71f548b975'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("update file set alias=file_name where alias is null")


def downgrade():
    op.execute("update file set alias=null")
