"""changed both pollvotes and opinionvotes

Revision ID: 0d08b17e8483
Revises: 85861a2f27b7
Create Date: 2019-04-18 18:06:41.917298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0d08b17e8483'
down_revision = '85861a2f27b7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('poll_votes', sa.Column('option_id', sa.Integer, sa.ForeignKey('options.id')))
    op.add_column('opinion_votes', sa.Column('option_id', sa.Integer, sa.ForeignKey('options.id')))

def downgrade():
    pass
