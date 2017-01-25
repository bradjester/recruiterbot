"""Added company_id field to all tables, added hiring_company field to job table

Revision ID: 0595d218001c
Revises: 58cfb037865e
Create Date: 2017-01-24 21:46:23.814971

"""
from alembic import op
import sqlalchemy as sa
from app.helpers import UTCDateTime


# revision identifiers, used by Alembic.
revision = '0595d218001c'
down_revision = '58cfb037865e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bots', sa.Column('company_id', sa.Integer(), nullable=False))
    op.create_foreign_key('bot_company_fk', 'bots', 'companies', ['company_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('candidates', sa.Column('company_id', sa.Integer(), nullable=False))
    op.create_foreign_key('candidate_company_fk', 'candidates', 'companies', ['company_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.add_column('jobs', sa.Column('hiring_company', sa.String(length=255), nullable=True))
    op.add_column('messages', sa.Column('company_id', sa.Integer(), nullable=False))
    op.create_foreign_key('message_company_fk', 'messages', 'companies', ['company_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')


def downgrade():
    op.drop_constraint('message_company_fk', 'messages', type_='foreignkey')
    op.drop_column('messages', 'company_id')
    op.drop_column('jobs', 'hiring_company')
    op.drop_constraint('candidate_company_fk', 'candidates', type_='foreignkey')
    op.drop_column('candidates', 'company_id')
    op.drop_constraint('bot_company_fk', 'bots', type_='foreignkey')
    op.drop_column('bots', 'company_id')
