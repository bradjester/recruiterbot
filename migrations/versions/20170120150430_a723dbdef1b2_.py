"""added tables : jobs, candidates, bots, messages

Revision ID: a723dbdef1b2
Revises: a10dc0b07f07
Create Date: 2017-01-20 15:04:30.594310

"""
from alembic import op
import sqlalchemy as sa
from app.helpers import UTCDateTime
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'a723dbdef1b2'
down_revision = 'a10dc0b07f07'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('companies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('jobs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('is_published', sa.Boolean(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('uuid', sa.String(length=36), nullable=False),
    sa.Column('jd_file_url', sa.String(length=1024), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.id'], name='job_company_fk', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('bots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('bot_id', sa.BigInteger(), nullable=False),
    sa.Column('bot_url', sa.String(length=1024), nullable=False),
    sa.Column('channel_type', sa.String(length=255), nullable=False),
    sa.Column('chat_type', sa.String(length=255), nullable=False),
    sa.ForeignKeyConstraint(['job_id'], ['jobs.id'], name='bot_job_fk', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bot_id')
    )
    op.create_table('candidates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('bot_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('resume_url', sa.String(length=1024), nullable=True),
    sa.Column('session_id', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['bot_id'], ['bots.id'], name='candidate_bot_fk', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', UTCDateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('bot_id', sa.BigInteger(), nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('received_at', mysql.DATETIME(fsp=3), nullable=False),
    sa.Column('sender', sa.String(length=255), nullable=False),
    sa.Column('receiver', sa.String(length=255), nullable=False),
    sa.Column('reply', mysql.TEXT(), nullable=False),
    sa.Column('reply_data', sa.String(length=1024), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=False),
    sa.Column('direction', sa.String(length=3), nullable=False),
    sa.Column('attached_media_url', sa.String(length=1024), nullable=True),
    sa.Column('secret', sa.String(length=1024), nullable=False),
    sa.ForeignKeyConstraint(['bot_id'], ['bots.bot_id'], name='message_bot_fk', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.id'], name='message_candidate_fk', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('roles', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('roles', 'updated_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.add_column('users', sa.Column('company_id', sa.Integer(), nullable=True))
    op.alter_column('users', 'confirmed_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'current_login_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('users', 'last_login_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=True)
    op.alter_column('users', 'updated_at',
               existing_type=mysql.DATETIME(),
               type_=UTCDateTime(timezone=True),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.create_foreign_key('user_company_fk', 'users', 'companies', ['company_id'], ['id'], onupdate='CASCADE', ondelete='SET NULL')


def downgrade():
    op.drop_constraint('user_company_fk', 'users', type_='foreignkey')
    op.alter_column('users', 'updated_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'last_login_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('users', 'current_login_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.alter_column('users', 'created_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('users', 'confirmed_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=True)
    op.drop_column('users', 'company_id')
    op.alter_column('roles', 'updated_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.alter_column('roles', 'created_at',
               existing_type=UTCDateTime(timezone=True),
               type_=mysql.DATETIME(),
               existing_nullable=False,
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_table('messages')
    op.drop_table('candidates')
    op.drop_table('bots')
    op.drop_table('jobs')
    op.drop_table('companies')