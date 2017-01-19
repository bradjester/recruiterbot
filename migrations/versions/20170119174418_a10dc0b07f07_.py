"""empty message

Revision ID: a10dc0b07f07
Revises: f34188271745
Create Date: 2017-01-19 17:44:18.661786

"""
from datetime import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a10dc0b07f07'
down_revision = 'f34188271745'
branch_labels = None
depends_on = None

user_role_name = 'user'
admin_role_name = 'admin'

roles_table = sa.table(
    'roles',
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False)
)


def upgrade():
    op.bulk_insert(
        roles_table,
        [
            {
                'name': user_role_name,
                'description': 'basic user role',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
            {
                'name': admin_role_name,
                'description': 'basic admin role',
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            },
        ]
    )


def downgrade():
    op.execute(roles_table.delete().where(
        sa.or_(roles_table.c.name == user_role_name,
               roles_table.c.name == admin_role_name)))
