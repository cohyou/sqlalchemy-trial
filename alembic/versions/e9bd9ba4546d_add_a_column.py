"""Add a column

Revision ID: e9bd9ba4546d
Revises: 231678912014
Create Date: 2020-01-09 11:32:26.991513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e9bd9ba4546d'
down_revision = '231678912014'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('column', sa.Column('last_trasaction_date', sa.DateTime))


def downgrade():
    op.drop_column('account', 'last_trasaction_date')
