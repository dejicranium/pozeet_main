"""add new_user ca
Revision ID: 85861a2f27b7
Revises: 78e744918768
Create Date: 2019-03-15 19:11:56.748239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '85861a2f27b7'
down_revision = '78e744918768'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('poll_votes', sa.Column('new_user', sa.Boolean, default=True))
        

def downgrade():
    pass
