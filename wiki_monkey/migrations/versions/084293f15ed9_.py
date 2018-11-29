"""empty message

Revision ID: 084293f15ed9
Revises: 256c0764ec9b
Create Date: 2018-09-24 16:22:00.316413

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select, delete, func

# This revision is practically reverted by d88cb486ef0d

# revision identifiers, used by Alembic.
revision = '084293f15ed9'
down_revision = '256c0764ec9b'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()

    # First delete all the records for each unique url except for the most
    # recent

    id = column('id', sa.Integer)
    url = column('url', sa.String)
    time_created = column('time_created', sa.DateTime)
    Bookmark = table('bookmark', url)

    deletable = []

    for row in conn.execute(
        select((url, )).select_from(Bookmark).group_by(url)
    ):
        deletable.extend([row['id'] for row in conn.execute(
            select((id, )).\
                select_from(Bookmark).\
                order_by(time_created.desc()).\
                where(url == row['url']).\
                offset(1)
        )])

    conn.execute(
        delete(Bookmark).where(id.in_(deletable))
    )

    # Add the UNIQUE constraint on the 'url' field
    # SQLite needs batch_alter_table()
    # http://alembic.zzzcomputing.com/en/latest/batch.html
    # https://www.sqlite.org/faq.html#q11
    with op.batch_alter_table(
        "bookmark",
        table_args=(sa.UniqueConstraint('url'), ),
    ) as batch_op:
        batch_op.create_unique_constraint('url', ['url'])


def downgrade():
    # SQLite needs batch_alter_table()
    # http://alembic.zzzcomputing.com/en/latest/batch.html
    # https://www.sqlite.org/faq.html#q11
    naming_convention = {
        "uq": "uq_%(table_name)s_%(column_0_name)s",
    }
    with op.batch_alter_table(
        "bookmark",
        naming_convention=naming_convention,
    ) as batch_op:
        batch_op.drop_constraint("uq_bookmark_url", type_="unique")
