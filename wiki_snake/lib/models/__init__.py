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

import os.path
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, init as fm_init, upgrade as fm_upgrade

from ..app import cliargs, app

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///' + os.path.abspath(cliargs.db_path))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database = SQLAlchemy(app)
migrate = Migrate(app, database)


def init_migrations():
    with app.app_context():
        fm_init()


def init_database():
    if not os.path.isfile(cliargs.db_path):
        # Don't use database.create_all(), let Alembic apply the initial
        # migration with the first upgrade below; only create the empty file
        # because the upgrade function doesn't do it
        # database.create_all()
        open(cliargs.db_path, 'a').close()

    with app.app_context():
        fm_upgrade()
