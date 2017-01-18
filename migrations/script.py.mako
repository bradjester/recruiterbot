"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
from app.helpers import UTCDateTime
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}


def upgrade():
    ${upgrades.replace('app.helpers.UTCDateTime', 'UTCDateTime') if upgrades else "pass"}


def downgrade():
    ${downgrades.replace('app.helpers.UTCDateTime', 'UTCDateTime') if downgrades else "pass"}
