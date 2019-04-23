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
    op.add_column('poll_votes', sa.Column('option_id', sa.Integer()))
    op.add_column('opinion_votes', sa.Column('option_id', sa.Integer(),))
    op.create_foreign_key('option_poll_user_fk', 'poll_votes', 'options', ['id'], ['id'])
    op.create_foreign_key('option_opinion_user_fk', 'opinion_votes', 'option', ['id'], ['id'])


def downgrade():
    op.drop_column('poll_votes', sa.Column('option_id', sa.Integer, sa.ForeignKey('options.id')))
    op.drop_column('opinion_votes', sa.Column('option_id', sa.Integer, sa.ForeignKey('options.id')))
