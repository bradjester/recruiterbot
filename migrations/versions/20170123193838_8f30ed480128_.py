"""added fields status and rating to candidates

Revision ID: 8f30ed480128
Revises: bd32bfd34482
Create Date: 2017-01-23 19:38:38.461370

"""
from alembic import op
import sqlalchemy as sa
from app.helpers import UTCDateTime


# revision identifiers, used by Alembic.
revision = '8f30ed480128'
down_revision = 'bd32bfd34482'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('candidates', sa.Column('rating', sa.Integer(), nullable=True))
    op.add_column('candidates', sa.Column('status', sa.String(length=255), nullable=False))


def downgrade():
    op.drop_column('candidates', 'status')
    op.drop_column('candidates', 'rating')
