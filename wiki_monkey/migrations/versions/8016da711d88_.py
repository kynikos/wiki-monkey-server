"""empty message

Revision ID: 8016da711d88
Revises: 982a3822ee72
Create Date: 2018-10-04 23:38:42.850048

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8016da711d88'
down_revision = '982a3822ee72'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bookmark', sa.Column('action_due', sa.String(), nullable=True))
    op.add_column('bookmark', sa.Column('notes', sa.Text(), nullable=True))
    op.add_column('bookmark', sa.Column('time_due', sa.DateTime(timezone=True), nullable=True))


def downgrade():
    # BUG: I don't think that drop_column works with SQLite
    op.drop_column('bookmark', 'time_due')
    op.drop_column('bookmark', 'notes')
    op.drop_column('bookmark', 'action_due')
