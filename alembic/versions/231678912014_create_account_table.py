"""create account table

Revision ID: 231678912014
Revises: 
Create Date: 2020-01-09 11:13:03.638741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '231678912014'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'account',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('description', sa.Unicode(200))
    )


def downgrade():
    op.drop_table('account')
