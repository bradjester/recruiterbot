"""Added expected_salary, work_type and location fields to the jobs table

Revision ID: 58cfb037865e
Revises: 8f30ed480128
Create Date: 2017-01-24 13:26:43.861912

"""
from alembic import op
import sqlalchemy as sa
from app.helpers import UTCDateTime


# revision identifiers, used by Alembic.
revision = '58cfb037865e'
down_revision = '8f30ed480128'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('jobs', sa.Column('expected_salary', sa.BigInteger(), nullable=True))
    op.add_column('jobs', sa.Column('location', sa.String(length=255), nullable=True))
    op.add_column('jobs', sa.Column('work_type', sa.String(length=255), nullable=True))


def downgrade():
    op.drop_column('jobs', 'work_type')
    op.drop_column('jobs', 'location')
    op.drop_column('jobs', 'expected_salary')
