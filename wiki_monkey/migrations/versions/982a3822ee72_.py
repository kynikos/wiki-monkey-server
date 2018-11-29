"""empty message

Revision ID: 982a3822ee72
Revises: 084293f15ed9
Create Date: 2018-09-30 17:29:40.002548

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '982a3822ee72'
down_revision = '084293f15ed9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('bookmark', sa.Column('section_id', sa.String(), nullable=True))
    op.add_column('bookmark', sa.Column('section_number', sa.Integer(), nullable=True))
    op.add_column('bookmark', sa.Column('section_title', sa.String(), nullable=True))


def downgrade():
    # BUG: I don't think that drop_column works with SQLite
    op.drop_column('bookmark', 'section_title')
    op.drop_column('bookmark', 'section_number')
    op.drop_column('bookmark', 'section_id')
