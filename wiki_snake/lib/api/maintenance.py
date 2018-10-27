# Wiki Snake - Wiki Monkey's database server
# Copyright (C) 2018 Dario Giovannetti <dev@dariogiovannetti.net>
#
# This file is part of Wiki Snake.
#
# Wiki Snake is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wiki Snake is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wiki Snake.  If not, see <http://www.gnu.org/licenses/>.

import flask_migrate as fm
import sqlalchemy as sa

from . import api
from ..app import VERSION
from ..models import database as db
ma = api.ma


class sInfo(api.Schema):
    version = ma.String()
    database_revision = ma.String()


class sUpgrade(api.Schema):
    success = ma.Boolean()
    noop = ma.Boolean()
    old_revision = ma.String()
    new_revision = ma.String()


def get_database_revision():
    # flask_migrate.current() prints to some kind of stream that I haven't
    # found a way to capture (no, not sys.stdout nor sys.stderr)
    return db.session.execute(
        sa.select(('version_num', )).\
        select_from('alembic_version')).\
        scalar()


maintenance = api.create_resource('Maintenance')


@maintenance.post(None, sUpgrade())
def upgrade_database(indata):
    """
    Upgrades the database to the latest revision.
    """
    old_revision = get_database_revision()
    fm.upgrade()
    new_revision = get_database_revision()
    return {
        'success': True,
        'noop': old_revision == new_revision,
        'old_revision': old_revision,
        'new_revision': new_revision,
    }


@maintenance.get(None, sInfo())
def info(indata):
    """
    Return some metadata.
    """
    return {
        'version': VERSION,
        'database_revision': get_database_revision(),
    }
