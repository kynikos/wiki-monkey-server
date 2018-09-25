"""empty message

Revision ID: 256c0764ec9b
Revises:
Create Date: 2018-09-24 14:49:35.543699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '256c0764ec9b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('bookmark',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('url', sa.String(), nullable=True),
        sa.Column('wgArticleId', sa.Integer(), nullable=True),
        sa.Column('wgPageName', sa.String(), nullable=True),
        sa.Column('wgRelevantPageName', sa.String(), nullable=True),
        sa.Column('wgCanonicalSpecialPageName', sa.String(), nullable=True),
        sa.Column('wgCanonicalNamespace', sa.String(), nullable=True),
        sa.Column('wgNamespaceNumber', sa.Integer(), nullable=True),
        sa.Column('wgTitle', sa.String(), nullable=True),
        sa.Column('wgRevisionId', sa.Integer(), nullable=True),
        sa.Column('wgCurRevisionId', sa.Integer(), nullable=True),
        sa.Column('wgDiffOldId', sa.Integer(), nullable=True),
        sa.Column('wgDiffNewId', sa.Integer(), nullable=True),
        sa.Column('wgAction', sa.String(), nullable=True),
        sa.Column('wgIsArticle', sa.Boolean(), nullable=True),
        sa.Column('wgIsProbablyEditable', sa.Boolean(), nullable=True),
        sa.Column('wgRelevantPageIsProbablyEditable', sa.Boolean(), nullable=True),
        sa.Column('wgPageContentLanguage', sa.String(), nullable=True),
        sa.Column('wgPageContentModel', sa.String(), nullable=True),
        sa.Column('time_created', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('time_updated', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('bookmark')
