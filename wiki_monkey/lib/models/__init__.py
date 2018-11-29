# Wiki Monkey's database server
# Copyright (C) 2018 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Monkey's database server.
#
# Wiki Monkey is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wiki Monkey is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wiki Monkey.  If not, see <http://www.gnu.org/licenses/>.

import os.path
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import (Migrate, init as fm_init, revision as fm_revision,
                           migrate as fm_migrate, upgrade as fm_upgrade)

from ..app import conf, app

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.abspath(conf['db_path']))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
migrate = Migrate(app, database, directory=os.path.join(
    os.path.dirname(__file__), '../../migrations'))

# TODO: Import/export tables from/to CSV/JSON


def init_migrations():
    with app.app_context():
        fm_init()


def create_revision():
    with app.app_context():
        fm_revision()


def create_migration():
    with app.app_context():
        fm_migrate()


def init_database():
    # TODO: Also test if it's a valid database
    if not os.path.isfile(conf['db_path']):
        # Don't use database.create_all(), let Alembic apply the initial
        # migration with the first upgrade below; only create the empty file
        # because the upgrade function doesn't do it
        # database.create_all()
        open(conf['db_path'], 'a').close()

    with app.app_context():
        fm_upgrade()


# SQLAlchemy doesn't support SQLite's ON CONFLICT DO UPDATE
# https://www.sqlite.org/lang_UPSERT.html
# TODO: ...yet? Check for updates
def upsert(table, fields, on_conflict):
    return sa.text('''
        INSERT INTO {table} ({fields})
        VALUES ({values})
        ON CONFLICT({on_conflict})
        DO UPDATE SET {fields_values}
    '''.format(
        table=table,
        fields=', '.join(fields),
        values=', '.join([''.join((':', f)) for f in fields]),
        on_conflict=', '.join(on_conflict),
        fields_values=', '.join(['=:'.join((f, f)) for f in fields]),
    ))
